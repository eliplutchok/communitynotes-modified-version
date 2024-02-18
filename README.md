# Community Notes

![](/documentation/images/help-rate-this-note-expanded.png)

## Welcome to Community Notes's revised addition by me

Please go here to see the original readme: https://github.com/twitter/communitynotes/tree/main?tab=readme-ov-file

This is a revised edition of community notes. It fixes some bugs, adds some extra functionality, and most importantly refactors parts of the code so that it will work well with more than one factor. In this readme, I just detail my changes.

1. Added a data folder, with some scripts.
2. In contants I add (in the beggining): numFactors and factorRegularizationRatio

Instructions to run program:

1. Navigate to data folder and download data using by editing the date in the download_data file and running it.
2. Edit num_factors in constants to whatever you want, default is 1.
3. Navigate back to the sourcecode directory and run the following command:
   python main.py \
    --enrollment data/userEnrollment-00000.tsv \
    --notes data/notes-00000.tsv \
    --ratings data/ratings \
    --status data/noteStatusHistory-00000.tsv \
    --outdir data
