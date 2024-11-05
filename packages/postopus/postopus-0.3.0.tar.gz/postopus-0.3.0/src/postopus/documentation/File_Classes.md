# File Classes for Postopus

Postopus automatically determines the correct class to load files from their suffix.
`octopus_inp_parser/file_meta_information/fileinfo.yaml` contains a mapping from Octopus' 'OutputFormat' parameter to the actual filetype suffix (`output_field_to_file_extension`).

For every file loader class, two fields are required: `EXTENSIONS` and `MAINCLASS`.
`EXTENSIONS` should contain all the file suffixes that can be opened by the class as a list.
`MAINCLASS` should contain the actual name of the class as a string.
From this, the correct class is derived and used for opening.
