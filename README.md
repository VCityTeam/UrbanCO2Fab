#UrbanCo2Fab
=========================

## init 
=========================
$ urbanco2fab init .

Initialize urbanco2fab directory. A .urbanco2fab directory along with .git will be created for managing the metadata.

## add
=========================
$ urbanco2fab add filename
Add a file to urbanco2fab (stage)

##commit
=========================
$ urbanco2fab commit --message "First commit" --time '1950-06-05T15:29:54+02:00,1954-06-05T15:29:54+02:00' --tag 'Building' --document building.txt

Note: Start time must be less than or equal to the end time of physical existence

Creates a new version with the specified timestamp of physical existence, associated tags and documents

$ urbanco2fab commit --message "First commit" --time '1950-06-05T15:29:54+02:00,1954-06-05T15:29:54+02:00' --tag 'Building' --document building.txt --versiontype existing

or 

$ urbanco2fab commit --message "First commit" --time '1950-06-05T15:29:54+02:00,1954-06-05T15:29:54+02:00' --tag 'Building' --document building.txt --versiontype imagined

Specify the type of version (imagined or existing)
