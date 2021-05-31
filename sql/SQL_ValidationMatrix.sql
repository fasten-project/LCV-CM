DROP TABLE IF EXISTS public.validationmatrix;
CREATE TABLE public.validationmatrix
(
    "License" TEXT,
    "Classpath exception to GPL 2.0 or later" bit,
    "GPL 2.0 or later" bit,
    "Apache 2.0" bit,
    "GPL 3.0" bit,
    PRIMARY KEY ("License")
);

ALTER TABLE public.validationmatrix
    OWNER to michelescarlato;

ALTER ROLE michelescarlato WITH SUPERUSER;

COMMENT ON TABLE public.validationmatrix
    IS 'This is the Validation Matrix used by the License Compliance Validator component. ';
