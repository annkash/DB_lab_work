CREATE EXTENSION IF NOT EXISTS dblink WITH SCHEMA public;
COMMENT ON EXTENSION dblink IS 'connect to other PostgreSQL databases from within a database';
CREATE FUNCTION public.calculate_final_cost() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
declare
  age integer;
  course_cost integer;
begin
  age := extract(year from NEW.enrollment_date) - extract(year from NEW.date_of_birth) - 
    case when extract(month from NEW.date_of_birth) > extract(month from NEW.enrollment_date) or
          (extract(month from NEW.date_of_birth) = extract(month from NEW.enrollment_date) and 
           extract(day from NEW.date_of_birth) >= extract(day from NEW.enrollment_date))
    then 1 else 0 end;
  if (extract(month from NEW.date_of_birth) < 3 or extract(month from NEW.date_of_birth) > 10) and
      extract(month from NEW.enrollment_date) < 3 then
        age := age - 1;
  end if;
  SELECT cost FROM study_cost WHERE category = NEW.category into course_cost;
  case
    when age < 18 then
        NEW.final_cost := course_cost * 0.8; 
    when age >= 18 and age < 25 and NEW.category = 'A' then
        NEW.final_cost := course_cost * 0.9; 
    else
        NEW.final_cost := course_cost; 
  end case;
  return new;
end;
$$;
ALTER FUNCTION public.calculate_final_cost() OWNER TO postgres;
CREATE FUNCTION public.create_db(dbname text) RETURNS void
    LANGUAGE plpgsql
    AS $$
BEGIN
IF EXISTS (SELECT 1 FROM pg_database WHERE datname = dbname) THEN
    RAISE NOTICE 'Database already exists';
  ELSE
    PERFORM dblink_connect('host=localhost user=postgres password=1234' || ' dbname=' || current_database());
    PERFORM dblink_exec('CREATE DATABASE ' || quote_ident(dbname) );
  END IF;
END
$$;
ALTER FUNCTION public.create_db(dbname text) OWNER TO postgres;
CREATE FUNCTION public.delete_by_address(search_value text) RETURNS void
    LANGUAGE plpgsql
    AS $$
BEGIN
    DELETE FROM students WHERE students.city = search_value;
END;
$$;
ALTER FUNCTION public.delete_by_address(search_value text) OWNER TO postgres;
CREATE FUNCTION public.delete_record_by_primary_key(table_name text, pk_column_name text, pk_value integer) RETURNS void
    LANGUAGE plpgsql
    AS $_$
BEGIN
    EXECUTE 'DELETE FROM ' || table_name || ' WHERE ' || pk_column_name || ' = $1' USING pk_value;
END;
$_$;
ALTER FUNCTION public.delete_record_by_primary_key(table_name text, pk_column_name text, pk_value integer) OWNER TO postgres;
CREATE FUNCTION public.delete_record_by_primary_key(table_name text, pk_column_name text, pk_value text) RETURNS void
    LANGUAGE plpgsql
    AS $_$
BEGIN
    EXECUTE 'DELETE FROM ' || table_name || ' WHERE ' || pk_column_name || ' = $1' USING pk_value;
END;
$_$;
ALTER FUNCTION public.delete_record_by_primary_key(table_name text, pk_column_name text, pk_value text) OWNER TO postgres;
CREATE FUNCTION public.drop_db(dbname text) RETURNS void
    LANGUAGE plpgsql
    AS $$
BEGIN
    PERFORM dblink_connect('host=localhost user=postgres password=1234' || ' dbname=' || current_database());
    PERFORM dblink_exec('DROP DATABASE ' || dbname);
END;
$$;
ALTER FUNCTION public.drop_db(dbname text) OWNER TO postgres;
CREATE FUNCTION public.full_database_cleaning(db_name text) RETURNS void
    LANGUAGE plpgsql
    AS $$
DECLARE
    tbl_record RECORD;
BEGIN
    FOR tbl_record IN (SELECT table_name FROM information_schema.tables WHERE table_schema NOT IN ('pg_catalog', 'information_schema')) LOOP
        EXECUTE 'TRUNCATE TABLE "' || tbl_record.table_name || '" CASCADE' USING db_name;
    END LOOP;
END;
$$;
ALTER FUNCTION public.full_database_cleaning(db_name text) OWNER TO postgres;
CREATE FUNCTION public.get_databases_names(OUT databases_names_text text) RETURNS text
    LANGUAGE plpgsql
    AS $$
BEGIN
    SELECT string_agg(datname, ',') INTO databases_names_text FROM pg_database;
END
$$;
ALTER FUNCTION public.get_databases_names(OUT databases_names_text text) OWNER TO postgres;
CREATE FUNCTION public.get_table_columns(tab_name text, database_name text) RETURNS text
    LANGUAGE plpgsql
    AS $$
BEGIN
  RETURN (SELECT string_agg(column_name, ',') FROM information_schema.columns
                    WHERE table_schema = 'public'
                    AND table_name = format('%s', tab_name) AND table_catalog = format('%s', database_name)) ;
END;
$$;
ALTER FUNCTION public.get_table_columns(tab_name text, database_name text) OWNER TO postgres;
CREATE FUNCTION public.get_table_columns_type(tab_name text, database_name text) RETURNS text
    LANGUAGE plpgsql
    AS $$
BEGIN
  RETURN (SELECT string_agg(data_type, ',') FROM information_schema.columns
                    WHERE table_schema = 'public'
                    AND table_name = format('%s', tab_name) AND table_catalog = format('%s', database_name)) ;
END;
$$;
ALTER FUNCTION public.get_table_columns_type(tab_name text, database_name text) OWNER TO postgres;
CREATE FUNCTION public.get_table_names(OUT table_names_text text) RETURNS text
    LANGUAGE plpgsql
    AS $$
BEGIN
    SELECT string_agg(table_name, ',') INTO table_names_text FROM information_schema.tables 
    WHERE table_type = 'BASE TABLE' AND table_schema = 'public';
END
$$;
ALTER FUNCTION public.get_table_names(OUT table_names_text text) OWNER TO postgres;
CREATE FUNCTION public.insert_data(tablename text, inputdata text) RETURNS void
    LANGUAGE plpgsql
    AS $$
DECLARE
    insertQuery TEXT;
BEGIN
    insertQuery := format('INSERT INTO %I VALUES (%s);', tableName, inputData);
    EXECUTE insertQuery;
END;
$$;
ALTER FUNCTION public.insert_data(tablename text, inputdata text) OWNER TO postgres;
CREATE FUNCTION public.one_table_cleaning(table_name text) RETURNS void
    LANGUAGE plpgsql
    AS $$
BEGIN
    EXECUTE 'DELETE FROM ' || table_name;
END;
$$;
ALTER FUNCTION public.one_table_cleaning(table_name text) OWNER TO postgres;
CREATE FUNCTION public.search_by_address(search_value text) RETURNS TABLE(student_id integer, surname character varying, name character varying, patronymic character varying, sex character varying, date_of_birth date, city character varying, street character varying, house character varying, flat character varying, telephone_number character varying, category character varying, enrollment_date date, final_cost numeric)
    LANGUAGE plpgsql
    AS $$
BEGIN
    RETURN QUERY
    SELECT * FROM students WHERE students.city = search_value;
END;
$$;
ALTER FUNCTION public.search_by_address(search_value text) OWNER TO postgres;
CREATE FUNCTION public.update_tuple(table_name text, column_name text, pk_column_name text, pk_value integer, new_value integer) RETURNS void
    LANGUAGE plpgsql
    AS $_$
BEGIN
    EXECUTE 'UPDATE ' || table_name || ' SET ' || column_name || ' = $1 WHERE ' || pk_column_name || ' = $2'  USING new_value, pk_value;
END;
$_$;
ALTER FUNCTION public.update_tuple(table_name text, column_name text, pk_column_name text, pk_value integer, new_value integer) OWNER TO postgres;
CREATE FUNCTION public.update_tuple(table_name text, column_name text, pk_column_name text, pk_value integer, new_value text) RETURNS void
    LANGUAGE plpgsql
    AS $_$
BEGIN
    EXECUTE 'UPDATE ' || table_name || ' SET ' || column_name || ' = $1 WHERE ' || pk_column_name || ' = $2'  USING new_value, pk_value;
END;
$_$;
ALTER FUNCTION public.update_tuple(table_name text, column_name text, pk_column_name text, pk_value integer, new_value text) OWNER TO postgres;
CREATE FUNCTION public.update_tuple(table_name text, column_name text, pk_column_name text, pk_value text, new_value integer) RETURNS void
    LANGUAGE plpgsql
    AS $_$
BEGIN
    EXECUTE 'UPDATE ' || table_name || ' SET ' || column_name || ' = $1 WHERE ' || pk_column_name || ' = $2'  USING new_value, pk_value;
END;
$_$;
ALTER FUNCTION public.update_tuple(table_name text, column_name text, pk_column_name text, pk_value text, new_value integer) OWNER TO postgres;
CREATE FUNCTION public.update_tuple(table_name text, column_name text, pk_column_name text, pk_value text, new_value text) RETURNS void
    LANGUAGE plpgsql
    AS $_$
BEGIN
    EXECUTE 'UPDATE ' || table_name || ' SET ' || column_name || ' = $1 WHERE ' || pk_column_name || ' = $2'  USING new_value, pk_value;
END;
$_$;
ALTER FUNCTION public.update_tuple(table_name text, column_name text, pk_column_name text, pk_value text, new_value text) OWNER TO postgres;
SET default_tablespace = '';
SET default_table_access_method = heap;
CREATE TABLE public.cars (
    car_id integer NOT NULL,
    model character varying(20) NOT NULL,
    year character varying(4) NOT NULL,
    license_plate character varying(10) NOT NULL
);
ALTER TABLE public.cars OWNER TO postgres;
CREATE TABLE public.exams (
    exam_id integer NOT NULL,
    student_id integer NOT NULL,
    instructor_id integer NOT NULL,
    date_of_exam date NOT NULL,
    result character varying(10),
    CONSTRAINT exams_result_check CHECK (((result)::text = ANY (ARRAY[('ñäàë'::character varying)::text, ('íå ñäàë'::character varying)::text])))
);
ALTER TABLE public.exams OWNER TO postgres;
CREATE TABLE public.instructors (
    instructor_id integer NOT NULL,
    car_id integer NOT NULL,
    surname character varying(20) NOT NULL,
    name character varying(20) NOT NULL,
    patronymic character varying(20) NOT NULL,
    sex character varying(10) NOT NULL,
    date_of_birth date NOT NULL,
    telephone_number character varying(15),
    category character varying(3) NOT NULL,
    CONSTRAINT instructors_category_check CHECK (((category)::text = ANY (ARRAY[('A'::character varying)::text, ('A1'::character varying)::text, ('B'::character varying)::text, ('B1'::character varying)::text, ('C'::character varying)::text, ('C1'::character varying)::text, ('D'::character varying)::text, ('D1'::character varying)::text, ('BE'::character varying)::text, ('CE'::character varying)::text, ('C1E'::character varying)::text, ('DE'::character varying)::text, ('D1E'::character varying)::text, ('M'::character varying)::text, ('Tm'::character varying)::text, ('Tb'::character varying)::text])))
);
ALTER TABLE public.instructors OWNER TO postgres;
CREATE TABLE public.students (
    student_id integer NOT NULL,
    surname character varying(20) NOT NULL,
    name character varying(20) NOT NULL,
    patronymic character varying(20) NOT NULL,
    sex character varying(10) NOT NULL,
    date_of_birth date NOT NULL,
    city character varying(40) NOT NULL,
    street character varying(40) NOT NULL,
    house character varying(10) NOT NULL,
    flat character varying(10),
    telephone_number character varying(15),
    category character varying(3) NOT NULL,
    enrollment_date date NOT NULL,
    final_cost numeric,
    CONSTRAINT students_category_check CHECK (((category)::text = ANY (ARRAY[('A'::character varying)::text, ('A1'::character varying)::text, ('B'::character varying)::text, ('B1'::character varying)::text, ('C'::character varying)::text, ('C1'::character varying)::text, ('D'::character varying)::text, ('D1'::character varying)::text, ('BE'::character varying)::text, ('CE'::character varying)::text, ('C1E'::character varying)::text, ('DE'::character varying)::text, ('D1E'::character varying)::text, ('M'::character varying)::text, ('Tm'::character varying)::text, ('Tb'::character varying)::text])))
);
ALTER TABLE public.students OWNER TO postgres;
CREATE TABLE public.study_cost (
    category character varying(3) NOT NULL,
    cost integer NOT NULL,
    CONSTRAINT study_cost_category_check CHECK (((category)::text = ANY (ARRAY[('A'::character varying)::text, ('B'::character varying)::text, ('C'::character varying)::text, ('D'::character varying)::text, ('BE'::character varying)::text, ('CE'::character varying)::text, ('DE'::character varying)::text, ('A1'::character varying)::text, ('B1'::character varying)::text, ('C1'::character varying)::text, ('D1'::character varying)::text, ('C1E'::character varying)::text, ('D1E'::character varying)::text])))
);
ALTER TABLE public.study_cost OWNER TO postgres;
ALTER TABLE ONLY public.cars
    ADD CONSTRAINT cars_license_plate_key UNIQUE (license_plate);
ALTER TABLE ONLY public.cars
    ADD CONSTRAINT cars_pkey PRIMARY KEY (car_id);
ALTER TABLE ONLY public.exams
    ADD CONSTRAINT exams_pkey PRIMARY KEY (exam_id);
ALTER TABLE ONLY public.instructors
    ADD CONSTRAINT instructors_car_id_key UNIQUE (car_id);
ALTER TABLE ONLY public.instructors
    ADD CONSTRAINT instructors_pkey PRIMARY KEY (instructor_id);
ALTER TABLE ONLY public.students
    ADD CONSTRAINT students_pkey PRIMARY KEY (student_id);
ALTER TABLE ONLY public.study_cost
    ADD CONSTRAINT study_cost_pkey PRIMARY KEY (category);
CREATE INDEX city ON public.students USING btree (city);
CREATE TRIGGER calculate_final_cost_trigger BEFORE INSERT ON public.students FOR EACH ROW EXECUTE FUNCTION public.calculate_final_cost();
ALTER TABLE ONLY public.exams
    ADD CONSTRAINT exams_instructor_id_fkey FOREIGN KEY (instructor_id) REFERENCES public.instructors(instructor_id) ON DELETE CASCADE;
ALTER TABLE ONLY public.exams
    ADD CONSTRAINT exams_student_id_fkey FOREIGN KEY (student_id) REFERENCES public.students(student_id) ON DELETE CASCADE;
ALTER TABLE ONLY public.instructors
    ADD CONSTRAINT instructors_car_id_fkey FOREIGN KEY (car_id) REFERENCES public.cars(car_id) ON DELETE CASCADE;
ALTER TABLE ONLY public.students
    ADD CONSTRAINT students_category_fkey FOREIGN KEY (category) REFERENCES public.study_cost(category) ON UPDATE CASCADE ON DELETE CASCADE;
GRANT SELECT,INSERT,DELETE,TRUNCATE,UPDATE ON TABLE public.cars TO user_role;
GRANT SELECT,INSERT,DELETE,TRUNCATE,UPDATE ON TABLE public.cars TO superuser;
GRANT SELECT,INSERT,DELETE,TRUNCATE,UPDATE ON TABLE public.exams TO user_role;
GRANT SELECT,INSERT,DELETE,TRUNCATE,UPDATE ON TABLE public.exams TO superuser;
GRANT SELECT,INSERT,DELETE,TRUNCATE,UPDATE ON TABLE public.instructors TO user_role;
GRANT SELECT,INSERT,DELETE,TRUNCATE,UPDATE ON TABLE public.instructors TO superuser;
GRANT SELECT,INSERT,DELETE,TRUNCATE,UPDATE ON TABLE public.students TO user_role;
GRANT SELECT,INSERT,DELETE,TRUNCATE,UPDATE ON TABLE public.students TO superuser;
GRANT SELECT,INSERT,DELETE,TRUNCATE,UPDATE ON TABLE public.study_cost TO user_role;
GRANT SELECT,INSERT,DELETE,TRUNCATE,UPDATE ON TABLE public.study_cost TO superuser;