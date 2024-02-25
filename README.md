# Community Notes

![](/documentation/images/help-rate-this-note-expanded.png)

## Welcome to Community Notes's Revised Addition by Me

Please go here to see the original readme: https://github.com/twitter/communitynotes/tree/main?tab=readme-ov-file

This is a revised edition of community notes. It fixes some bugs, adds some extra functionality, and most importantly refactors parts of the code so that it will work with more than one factor. In this readme, I detail my changes.

Changes required to get the code to run on a gpu:

1. Added `self.device` to cuda in matrix_factorization (line 88) also changed lines 214-219.
2. Added `self.device` to cuda in normalized_loss.
3. In normalized_loss I added `.cpu()` on line 108.

Changes required to handle multiple factors:

1. In constants I add (in the beggining): numFactors and interceptRegularizationDampener (by default set to numFactors).
2. Additional constants that I added:
   - `coreNoteFactorKeyBase`
   - `coreRaterFactorKeyBase`
   - `expansionNoteFactorKeyBase`
   - `expansionPlusNoteFactorKeyBase`
   - `groupNoteFactorKeyBase`
   - `groupRaterFactorKeyBase`
3. Edited `raterModelOutputTSVColumnsAndTypes` and `noteModelOutputTSVColumnsAndTypes` in constants.
4. Edited the following files and functions to handle multiple factors of notes and raters:
   - mf_base_scorer -> `get_scored_notes_cols`, `get_helpfulness_scores_cols`
   - mf_core_scorer -> `_get_note_col_mapping`, `_get_user_col_mapping`, `get_scored_notes_cols`, `get_helpfulness_scores_cols`
   - mf_expansion_scorer -> `get_scored_notes_cols`, `_get_dropped_user_cols`
   - mf_expansion_plus_scorer -> `get_scored_notes_cols`, `_get_note_col_mapping`, `_get_dropped_user_cols`
   - mf_group_scorer -> `coalesce_group_models`, `MFGroupScorer`, `MFGroupScorer` -> `_get_note_col_mapping`, `MFGroupScorer` -> `_get_user_col_mapping`, `MFGroupScorer` -> `get_scored_notes_cols`, `MFGroupScorer` -> `get_helpfulness_scores_cols`
   - note_ratings -> `compute_scored_notes`
   - note_ratings -> `is_crnh_diamond`
5. Edited matrix_factorization:
   Set `numFactors` to `c.numFactors`. Divided the 5s in the intercept lambdas by our new variable `interceptRegularizationDampener`.
6. Edited run_scoring, the initiation of the `MFGroupScorer` that uses `diamond_lambda`. I added in the `interceptRegularizationDampener` in the appropriate places.

Additional Changes:

1. Added data folder.
2. In the data folder I added a script that downloads all the necessary data.
3. I added/will add additional programs as well to help the user get a feel for the data.
4. Edited file names in runner.py to dynamically reflect the number of factors and interceptRegularizationDampener used.

Instructions to run program:

1. Install requirements `pip install -r requirements.txt` (first set up virtual env if your doing this on your own pc or gpu).
2. Navigate to data folder and download data using by editing the date in the download_data file and running it.
3. Edit num_factors in constants to whatever you want, default is 1.
4. Navigate back to the sourcecode directory and run the following command:
   ```bash
   python main.py \
    --enrollment data/userEnrollment-00000.tsv \
    --notes data/notes-00000.tsv \
    --ratings data/ratings \
    --status data/noteStatusHistory-00000.tsv \
    --outdir data
   ```
