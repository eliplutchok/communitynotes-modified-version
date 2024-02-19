# Community Notes

![](/documentation/images/help-rate-this-note-expanded.png)

## Welcome to Community Notes's revised addition by me

Please go here to see the original readme: https://github.com/twitter/communitynotes/tree/main?tab=readme-ov-file

This is a revised edition of community notes. It fixes some bugs, adds some extra functionality, and most importantly refactors parts of the code so that it will work well with more than one factor. In this readme, I just detail my changes.

1. Added a data folder, with some scripts.
2. Added self.device to cuda in matrix_factorization (line 88) also changed lines 214-219.
3. In normalized_loss I added .cpu() on line 108
4. In constants I add (in the beggining): numFactors and factorRegularizationRatio.
5. Additional constants that I added:
   coreNoteFactorKeyBase
   coreRaterFactorKeyBase

6. Edited the following files and functions to handle multiple factors of rnotes and raters:
   mf_base_scorer -> get_scored_notes_cols, get_helpfulness_scores_cols
   mf_core_scorer -> \_get_note_col_mapping, \_get_user_col_mapping, get_scored_notes_cols, get_helpfulness_scores_cols

Instructions to run program:

1. Install requirements (first set up virtual env if your doing this on your own pc or gpu).
2. Navigate to data folder and download data using by editing the date in the download_data file and running it.
3. Edit num_factors in constants to whatever you want, default is 1.
4. Navigate back to the sourcecode directory and run the following command:
   python main.py \
    --enrollment data/userEnrollment-00000.tsv \
    --notes data/notes-00000.tsv \
    --ratings data/ratings \
    --status data/noteStatusHistory-00000.tsv \
    --outdir data
