# Community Notes

![](/documentation/images/help-rate-this-note-expanded.png)

## Welcome to Community Notes's revised addition by me

Please go here to see the original readme: https://github.com/twitter/communitynotes/tree/main?tab=readme-ov-file

This is a revised edition of community notes. It fixes some bugs, adds some extra functionality, and most importantly refactors parts of the code so that it will work well with more than one factor. In this readme, I just detail my changes.

Changes required to get the code to run on a gpu:

1. Added self.device to cuda in matrix_factorization (line 88) also changed lines 214-219.
2. Added self.device to cude in normalized_loss
3. In normalized_loss I added .cpu() on line 108

Changes required to handle multiple factors:

1. In constants I add (in the beggining): numFactors and interceptRegularizationDampener (by default set to numFactors).
2. Additional constants that I added:
   - coreNoteFactorKeyBase
   - coreRaterFactorKeyBase
   - expansionNoteFactorKeyBase
   - expansionPlusNoteFactorKeyBase
   - groupNoteFactorKeyBase
   - groupRaterFactorKeyBase
3. Edited raterModelOutputTSVColumnsAndTypes in constants.
4. Edited the following files and functions to handle multiple factors of notes and raters:
   - mf_base_scorer -> get_scored_notes_cols, get_helpfulness_scores_cols
   - mf_core_scorer -> \_get_note_col_mapping, \_get_user_col_mapping, get_scored_notes_cols, get_helpfulness_scores_cols
   - mf_expansion_scorer -> get_scored_notes_cols, \_get_dropped_user_cols
   - mf_expansion_plus_scorer -> get_scored_notes_cols, \_get_dropped_note_cols
   - mf_group_scorer -> coalesce_group_models, MFGroupScorer, MFGroupScorer->\_get_note_col_mapping, MFGroupScorer->\_get_user_col_mapping, MFGroupScorer->get_scored_notes_cols, MFGroupScorer->get_helpfulness_scores_cols
   - note_ratings->compute_scored_notes
5. Edited matrix_factorization:
   Set numFactors to c.numFactors. Divided the 5s in the intercept lambdas by our new variable interceptRegularizationDampener.
6. Edited run_scoring, the initiation of the MFGroupScorer that uses diamond_lambda. I added in the interceptRegularizationDampener in the appropriate places.

Additional Changes:

1. Added data folder.
1. in the data folder I added a script that downloads all the necessary data.

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

getting this error, need to refactor that part of code, don't have time tonight, will do in a few days:
Traceback (most recent call last):
File "/home/ubuntu/CN-Revised/sourcecode/main.py", line 27, in <module>
main()
File "/home/ubuntu/CN-Revised/sourcecode/scoring/runner.py", line 96, in main
scoredNotes, helpfulnessScores, newStatus, auxNoteInfo = run_scoring(
File "/home/ubuntu/CN-Revised/sourcecode/scoring/run_scoring.py", line 661, in run_scoring
scoredNotes, helpfulnessScores, auxiliaryNoteInfo = \_run_scorers(
File "/home/ubuntu/CN-Revised/sourcecode/scoring/run_scoring.py", line 231, in \_run_scorers
modelResultsAndTimes = [
File "/home/ubuntu/CN-Revised/sourcecode/scoring/run_scoring.py", line 232, in <listcomp>
\_run_scorer_parallelizable(
File "/home/ubuntu/CN-Revised/sourcecode/scoring/run_scoring.py", line 179, in \_run_scorer_parallelizable
result = ModelResult(\*scorer.score(ratings, noteStatusHistory, userEnrollment))
File "/home/ubuntu/CN-Revised/sourcecode/scoring/scorer.py", line 173, in score
noteScores, userScores = self.\_score_notes_and_users(
File "/home/ubuntu/CN-Revised/sourcecode/scoring/mf_base_scorer.py", line 394, in \_score_notes_and_users
scoredNotes = note_ratings.compute_scored_notes(
File "/home/ubuntu/CN-Revised/sourcecode/scoring/note_ratings.py", line 523, in compute_scored_notes
scoredNotes = scoring_rules.apply_scoring_rules(
File "/home/ubuntu/CN-Revised/sourcecode/scoring/scoring_rules.py", line 780, in apply_scoring_rules
noteStatusUpdates, additionalColumns = rule.score_notes(noteStats, noteLabels, statusColumn)
File "/home/ubuntu/CN-Revised/sourcecode/scoring/scoring_rules.py", line 160, in score_notes
mask = self.\_function(noteStats)
File "/home/ubuntu/CN-Revised/sourcecode/scoring/note_ratings.py", line 440, in <lambda>
lambda noteStats: is_crnh_diamond_function(
File "/home/ubuntu/CN-Revised/sourcecode/scoring/note_ratings.py", line 37, in is_crnh_diamond
scoredNotes[c.internalNoteInterceptKey]
File "/home/ubuntu/.local/lib/python3.10/site-packages/pandas/core/ops/common.py", line 76, in new_method
return method(self, other)
File "/home/ubuntu/.local/lib/python3.10/site-packages/pandas/core/arraylike.py", line 60, in **ge**
return self.\_cmp_method(other, operator.ge)
File "/home/ubuntu/.local/lib/python3.10/site-packages/pandas/core/frame.py", line 7628, in \_cmp_method
self, other = self.\_align_for_op(other, axis, flex=False, level=None)
File "/home/ubuntu/.local/lib/python3.10/site-packages/pandas/core/frame.py", line 7936, in \_align_for_op
raise ValueError(
ValueError: Operands are not aligned. Do `left, right = left.align(right, axis=1, copy=False)` before operating.
