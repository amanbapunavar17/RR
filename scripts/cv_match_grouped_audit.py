import sys, os
sys.path.append(os.path.abspath('.'))
import pandas as pd
import numpy as np
from scipy.optimize import minimize

# Load audited data from previous step
from scripts.audit_win_prob_model import inn2, f1, log_loss_fn, sigmoid

# Grouped Cross-Validation by match_id
unique_matches = inn2['match_id'].unique()
np.random.seed(42)
np.random.shuffle(unique_matches)

# 5-fold match-grouped split
n_splits = 5
folds = np.array_split(unique_matches, n_splits)

cv_brier_scores = []
cv_log_losses = []

print(f"\n--- 5-FOLD MATCH-GROUPED CROSS-VALIDATION (Total Matches: {len(unique_matches)}) ---")
for fold_idx in range(n_splits):
    test_matches = set(folds[fold_idx])
    train_matches = set(unique_matches) - test_matches
    
    train_df = inn2[inn2['match_id'].isin(train_matches)].copy()
    test_df = inn2[inn2['match_id'].isin(test_matches)].copy()
    
    # Standardize based on TRAIN set only (no data leakage)
    X_train_raw = train_df[f1]
    train_mean = X_train_raw.mean()
    train_std = X_train_raw.std()
    
    X_tr = ((X_train_raw - train_mean) / train_std).values
    X_tr_mat = np.column_stack([np.ones(len(X_tr)), X_tr])
    y_tr = train_df['chase_won'].values
    
    X_te = ((test_df[f1] - train_mean) / train_std).values
    X_te_mat = np.column_stack([np.ones(len(X_te)), X_te])
    y_te = test_df['chase_won'].values
    
    res = minimize(log_loss_fn, np.zeros(X_tr_mat.shape[1]), args=(X_tr_mat, y_tr), method='BFGS')
    w_fold = res.x
    
    preds_te = sigmoid(np.dot(X_te_mat, w_fold))
    brier_te = np.mean((y_te - preds_te) ** 2)
    log_loss_te = -np.mean(y_te * np.log(np.clip(preds_te, 1e-12, 1-1e-12)) + (1 - y_te) * np.log(np.clip(1 - preds_te, 1e-12, 1-1e-12)))
    
    cv_brier_scores.append(brier_te)
    cv_log_losses.append(log_loss_te)
    print(f"Fold {fold_idx + 1} ({len(test_matches)} test matches, {len(test_df)} deliveries): Out-of-Sample Brier = {brier_te:.4f}, Log-Loss = {log_loss_te:.4f}")

mean_cv_brier = np.mean(cv_brier_scores)
mean_cv_log_loss = np.mean(cv_log_losses)
print(f"\nMean Out-of-Sample Match-Grouped Brier Score: {mean_cv_brier:.4f}")
print(f"Mean Out-of-Sample Match-Grouped Log-Loss: {mean_cv_log_loss:.4f}")
