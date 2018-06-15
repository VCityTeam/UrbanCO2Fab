# UrbanCo2Fab

## init 
<pre>
$ urbanco2fab init . --bare
</pre>

creates a bare repository (especially main repository).

<pre>
$ urbanco2fab init .
</pre>

Initialize urbanco2fab directory. 

In both cases, a .urbanco2fab directory along with .git will be created for managing the metadata.

## clone
<pre>
$ urbanco2fab clone URL
</pre>

clones a urbanco2fab workspace to the current directory.

## add
<pre>
$ urbanco2fab add filename
</pre>
Add a (CityGML) file to urbanco2fab (stage)

## commit
<pre>
$ urbanco2fab commit --message "First commit" --time '1950-06-05T15:29:54+02:00,1954-06-05T15:29:54+02:00' --tag 'Building' --document building.txt
</pre>

Note: Start time must be less than or equal to the end time of physical existence

Creates a new version with the specified timestamp of physical existence, associated tags and documents.

Specify the type of version (imagined or existing)

<pre>
$ urbanco2fab commit --message "First commit" --time '1950-06-05T15:29:54+02:00,1954-06-05T15:29:54+02:00' --tag 'Building' --document building.txt --versiontype existing
</pre>

or 

<pre>
$ urbanco2fab commit --message "First commit" --time '1950-06-05T15:29:54+02:00,1954-06-05T15:29:54+02:00' --tag 'Building' --document building.txt --versiontype imagined
</pre>

<pre>
$  urbanco2fab commit  --tag 'Building' --document building.txt --scenariotype consensus --scenario "First scenario" --version 70256c32c6f15b233a0ee84b85116df218229df8 dc3872a240d8edd6b07142a2b5dbd4b1c4d12985  --versiontransition 70256c32c6f15b233a0ee84b85116df218229df8:dc3872a240d8edd6b07142a2b5dbd4b1c4d12985
</pre>

creates a scenario with two versions

<pre>
$ urbanco2fab commit -c 'scenario1' -p scenario3
</pre>
creates a workspace with two scenarios

## show
<pre>
$ urbanco2fab show
</pre>
show the details of the current workspace

<pre>
$ urbanco2fab show -v all
</pre>

show all the versions

<pre>
$ urbanco2fab show -v 02a2a303390d788f465e33232b5892d73caaa239 eef7413c535c616ec13007f8878a885313bd8bd8 
</pre>

shows the details of two specified versions

## log

<pre>
$ urbanco2fab log -hs
</pre>
shows all the versions whose physical existence time ends before the current date.

<pre>
$ urbanco2fab log -hs -i 1955-06-05T15:29:54+02:00
</pre>
shows all the versions whose physical existence time ends before 1955-06-05T15:29:54+02:00.

<pre>
$ urbanco2fab log -fu -i 1955-06-05T15:29:54+02:00
</pre>
shows all the versions whose physical existence time starts after 1955-06-05T15:29:54+02:00.

<pre>
$ urbanco2fab log -fu 
</pre>
shows all the versions whose physical existence time starts after the current date.
