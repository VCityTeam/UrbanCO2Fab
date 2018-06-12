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

## commit
=========================
$ urbanco2fab commit --message "First commit" --time '1950-06-05T15:29:54+02:00,1954-06-05T15:29:54+02:00' --tag 'Building' --document building.txt

Note: Start time must be less than or equal to the end time of physical existence

Creates a new version with the specified timestamp of physical existence, associated tags and documents.

Specify the type of version (imagined or existing)

$ urbanco2fab commit --message "First commit" --time '1950-06-05T15:29:54+02:00,1954-06-05T15:29:54+02:00' --tag 'Building' --document building.txt --versiontype existing

or 

$ urbanco2fab commit --message "First commit" --time '1950-06-05T15:29:54+02:00,1954-06-05T15:29:54+02:00' --tag 'Building' --document building.txt --versiontype imagined

## show
=========================
$ urbanco2fab show -v all

show all the versions

$ urbanco2fab show -v 02a2a303390d788f465e33232b5892d73caaa239 eef7413c535c616ec13007f8878a885313bd8bd8 

shows the details of two specified versions
