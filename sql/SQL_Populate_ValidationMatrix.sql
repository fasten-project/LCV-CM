TRUNCATE public.validationmatrix;
COPY public.validationmatrix("License","Classpath exception to GPL 2.0 or later", "GPL 2.0 or later","Apache 2.0", "GPL 3.0")
FROM '/home/michelescarlato/licenses.csv'
DELIMITER ','
CSV HEADER;
