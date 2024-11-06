from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, AdaBoostClassifier,BaggingClassifier
from sklearn.svm import SVC
from sklearn.calibration import CalibratedClassifierCV
from sklearn.model_selection import GridSearchCV,StratifiedKFold
from sklearn.linear_model import LassoCV, LogisticRegression, Lasso, Ridge,RidgeClassifierCV, ElasticNet
from sklearn.feature_selection import RFE
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
import xgboost as xgb  # Make sure you have xgboost installed

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import (accuracy_score, precision_score, recall_score, 
                             f1_score, roc_auc_score, confusion_matrix,
                             matthews_corrcoef,roc_curve,auc,
                             balanced_accuracy_score,precision_recall_curve,average_precision_score)
from imblearn.over_sampling import SMOTE
from sklearn.pipeline import Pipeline
from collections import defaultdict
from sklearn.preprocessing import StandardScaler
from typing import Dict, Any, Optional,List
import numpy as np
import pandas as pd
from . import ips 
from . import plot
import matplotlib.pyplot as plt
import seaborn as sns
plt.style.use("paper") 
import logging
import warnings
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

# Ignore specific warnings (UserWarning in this case)
warnings.filterwarnings("ignore", category=UserWarning)
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier

def features_knn(X_train: pd.DataFrame, y_train: pd.Series, knn_params: dict) -> pd.DataFrame:
    """
    A distance-based classifier that assigns labels based on the majority label of nearest neighbors.
    when to use:
        Effective for small to medium datasets with a low number of features.
        It does not directly provide feature importances but can be assessed through feature permutation or similar methods.
    Recommended Use: Effective for datasets with low feature dimensionality and well-separated clusters.

    Fits KNeighborsClassifier and approximates feature influence using permutation importance.
    """
    knn = KNeighborsClassifier(**knn_params)
    knn.fit(X_train, y_train)
    importances = permutation_importance(knn, X_train, y_train, n_repeats=30, random_state=1, scoring="accuracy")
    return pd.DataFrame({"feature": X_train.columns, "importance": importances.importances_mean}).sort_values(by="importance", ascending=False)

#! 1. Linear and Regularized Regression Methods
# 1.1 Lasso
def features_lasso(X_train: pd.DataFrame, y_train: pd.Series, lasso_params: dict) -> np.ndarray:
    """
    Lasso (Least Absolute Shrinkage and Selection Operator): 
    A regularized linear regression method that uses L1 penalty to shrink coefficients, effectively 
    performing feature selection by zeroing out less important ones.
    """
    lasso = LassoCV(**lasso_params)
    lasso.fit(X_train, y_train)
    # Get non-zero coefficients and their corresponding features
    coefficients = lasso.coef_
    importance_df = pd.DataFrame({
        "feature": X_train.columns,
        "importance": np.abs(coefficients)
    }) 
    return importance_df[importance_df["importance"] > 0].sort_values(by="importance", ascending=False)

# 1.2 Ridge regression
def features_ridge(X_train: pd.DataFrame, y_train: pd.Series, ridge_params: dict) -> np.ndarray:
    """
    Ridge Regression: A linear regression technique that applies L2 regularization, reducing coefficient 
    magnitudes to avoid overfitting, especially with multicollinearity among features.
    """
    from sklearn.linear_model import RidgeCV
    ridge = RidgeCV(**ridge_params)
    ridge.fit(X_train, y_train)
    
    # Get the coefficients
    coefficients = ridge.coef_
    
    # Create a DataFrame to hold feature importance
    importance_df = pd.DataFrame({
        "feature": X_train.columns,
        "importance": np.abs(coefficients)
    }) 
    return importance_df[importance_df["importance"] > 0].sort_values(by="importance", ascending=False)

# 1.3 Elastic Net(Enet)
def features_enet(X_train: pd.DataFrame, y_train: pd.Series, enet_params: dict) -> np.ndarray:
    """
    Elastic Net (Enet): Combines L1 and L2 penalties (lasso and ridge) in a linear model, beneficial 
    when features are highly correlated or for datasets with more features than samples.
    """
    from sklearn.linear_model import ElasticNetCV
    enet = ElasticNetCV(**enet_params)
    enet.fit(X_train, y_train)
    # Get the coefficients
    coefficients = enet.coef_
    # Create a DataFrame to hold feature importance
    importance_df = pd.DataFrame({
        "feature": X_train.columns,
        "importance": np.abs(coefficients)
    })
    return importance_df[importance_df["importance"] > 0].sort_values(by="importance", ascending=False)
# 1.4 Partial Least Squares Regression for Generalized Linear Models (plsRglm): Combines regression and 
# feature reduction, useful for high-dimensional data with correlated features, such as genomics.

#! 2.Generalized Linear Models and Extensions
# 2.1 

#!3.Tree-Based and Ensemble Methods
# 3.1 Random Forest(RF)
def features_rf(X_train: pd.DataFrame, y_train: pd.Series, rf_params: dict) -> np.ndarray:
    """
    An ensemble of decision trees that combines predictions from multiple trees for classification or 
    regression, effective with high-dimensional, complex datasets.
    when to use:
        Handles high-dimensional data well.
        Robust to overfitting due to averaging of multiple trees.
        Provides feature importance, which can help in understanding the influence of different genes.
    Fit Random Forest and return sorted feature importances.
    Recommended Use: Great for classification problems, especially when you have many features (genes).
    """
    rf = RandomForestClassifier(**rf_params)
    rf.fit(X_train, y_train)
    return pd.DataFrame({"feature": X_train.columns, "importance": rf.featuress_}).sort_values(by="importance", ascending=False)
# 3.2 Gradient Boosting Trees
def features_gradient_boosting(X_train: pd.DataFrame, y_train: pd.Series, gb_params: dict) -> pd.DataFrame:
    """
    An ensemble of decision trees that combines predictions from multiple trees for classification or regression, effective with 
    high-dimensional, complex datasets.
    Gradient Boosting
    Strengths:
        High predictive accuracy and works well for both classification and regression.
        Can handle a mixture of numerical and categorical features.
    Recommended Use: 
        Effective for complex relationships and when you need a powerful predictive model.
    Fit Gradient Boosting classifier and return sorted feature importances.
    Recommended Use: Effective for complex datasets with many features (genes).
    """
    gb = GradientBoostingClassifier(**gb_params)
    gb.fit(X_train, y_train)
    return pd.DataFrame({"feature": X_train.columns, "importance": gb.feature_importances_}).sort_values(by="importance", ascending=False)
# 3.3 XGBoost
def features_xgb(X_train: pd.DataFrame, y_train: pd.Series, xgb_params: dict) -> pd.DataFrame:
    """
    XGBoost: An advanced gradient boosting technique, faster and more efficient than GBM, with excellent predictive performance on structured data.
    """
    import xgboost as xgb
    xgb_model = xgb.XGBClassifier(**xgb_params)
    xgb_model.fit(X_train, y_train)
    return pd.DataFrame({"feature": X_train.columns, "importance": xgb_model.feature_importances_}).sort_values(by="importance", ascending=False)
# 3.4.decision tree
def features_decision_tree(X_train: pd.DataFrame, y_train: pd.Series, dt_params: dict) -> pd.DataFrame:
    """
    A single decision tree classifier effective for identifying key decision boundaries in data.
    when to use:
        Good for capturing non-linear patterns.
        Provides feature importance scores for each feature, though it may overfit on small datasets.
        Efficient for low to medium-sized datasets, where interpretability of decisions is key.
    Recommended Use: Useful for interpretable feature importance analysis in smaller or balanced datasets.
    
    Fits DecisionTreeClassifier and returns sorted feature importances.
    """
    dt = DecisionTreeClassifier(**dt_params)
    dt.fit(X_train, y_train)
    return pd.DataFrame({"feature": X_train.columns, "importance": dt.feature_importances_}).sort_values(by="importance", ascending=False)
# 3.5 bagging
def features_bagging(X_train: pd.DataFrame, y_train: pd.Series, bagging_params: dict) -> pd.DataFrame:
    """
    A bagging ensemble of classifiers, often used with weak learners like decision trees, to reduce variance.
    when to use:
        Helps reduce overfitting, especially on high-variance models.
        Effective when the dataset has numerous features and may benefit from ensemble stability.
    Recommended Use: Beneficial for high-dimensional or noisy datasets needing ensemble stability.
    
    Fits BaggingClassifier and returns averaged feature importances from underlying estimators if available.
    """
    bagging = BaggingClassifier(**bagging_params)
    bagging.fit(X_train, y_train)
    
    # Calculate feature importance by averaging importances across estimators, if feature_importances_ is available.
    if hasattr(bagging.estimators_[0], "feature_importances_"):
        importances = np.mean([estimator.feature_importances_ for estimator in bagging.estimators_], axis=0)
        return pd.DataFrame({"feature": X_train.columns, "importance": importances}).sort_values(by="importance", ascending=False)
    else:
        # If the base estimator does not support feature importances, fallback to permutation importance.
        importances = permutation_importance(bagging, X_train, y_train, n_repeats=30, random_state=1, scoring="accuracy")
        return pd.DataFrame({"feature": X_train.columns, "importance": importances.importances_mean}).sort_values(by="importance", ascending=False)

#! 4.Support Vector Machines
def features_svm(X_train: pd.DataFrame, y_train: pd.Series, rfe_params: dict) -> np.ndarray:
    """
    Suitable for classification tasks where the number of features is much larger than the number of samples.
        1. Effective in high-dimensional spaces and with clear margin of separation.
        2. Works well for both linear and non-linear classification (using kernel functions).
    Select features using RFE with SVM.When combined with SVM, RFE selects features that are most critical for the decision boundary, 
        helping reduce the dataset to a more manageable size without losing much predictive power.
    SVM (Support Vector Machines),supports various kernels (linear, rbf, poly, and sigmoid), is good at handling high-dimensional 
        data and finding an optimal decision boundary between classes, especially when using the right kernel.
    kernel: ["linear", "rbf", "poly", "sigmoid"]
        'linear': simplest kernel that attempts to separate data by drawing a straight line (or hyperplane) between classes. It is effective 
            when the data is linearly separable, meaning the classes can be well divided by a straight boundary.
                Advantages:
                    - Computationally efficient for large datasets.
                    - Works well when the number of features is high, which is common in genomic data where you may have thousands of genes 
                        as features.
        'rbf':  a nonlinear kernel that maps the input data into a higher-dimensional space to find a decision boundary. It works well for 
            data that is not linearly separable in its original space.
                Advantages: 
                    - Handles nonlinear relationships between features and classes
                    - Often better than a linear kernel when there is no clear linear decision boundary in the data.
        'poly': Polynomial Kernel: computes similarity between data points based on polynomial functions of the input features. It can model 
            interactions between features to a certain degree, depending on the polynomial degree chosen.
                Advantages:
                    - Allows modeling of feature interactions.
                    - Can fit more complex relationships compared to linear models.
        'sigmoid':  similar to the activation function in neural networks, and it works well when the data follows an S-shaped decision boundary.
                Advantages:
                - Can approximate the behavior of neural networks.
                - Use case: It’s not as widely used as the RBF or linear kernel but can be explored when there is some evidence of non-linear 
                    S-shaped relationships.
    """
    # SVM (Support Vector Machines)
    svc = SVC(kernel=rfe_params["kernel"]) # ["linear", "rbf", "poly", "sigmoid"]
    # RFE(Recursive Feature Elimination)
    selector = RFE(svc, n_features_to_select=rfe_params["n_features_to_select"])
    selector.fit(X_train, y_train)
    return X_train.columns[selector.support_]
#! 5.Bayesian and Probabilistic Methods
def features_naive_bayes(X_train: pd.DataFrame, y_train: pd.Series) -> list:
    """
    Naive Bayes: A probabilistic classifier based on Bayes' theorem, assuming independence between features, simple and fast, especially 
    effective for text classification and other high-dimensional data.
    """
    from sklearn.naive_bayes import GaussianNB
    nb = GaussianNB()
    nb.fit(X_train, y_train)
    probabilities = nb.predict_proba(X_train)
    return X_train.columns[np.argsort(probabilities.max(axis=1))[:X_train.shape[1] // 2]]
#! 6.Linear Discriminant Analysis (LDA)
def features_lda(X_train: pd.DataFrame, y_train: pd.Series) -> list:
    """
    Linear Discriminant Analysis (LDA): Projects data onto a lower-dimensional space to maximize class separability, often used as a dimensionality 
    reduction technique before classification on high-dimensional data.
    """
    from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
    lda = LinearDiscriminantAnalysis()
    lda.fit(X_train, y_train)
    coef = lda.coef_.flatten()
    # Create a DataFrame to hold feature importance
    importance_df = pd.DataFrame({
        "feature": X_train.columns,
        "importance": np.abs(coef)
    }) 
    
    return importance_df[importance_df["importance"] > 0].sort_values(by="importance", ascending=False)

def features_adaboost(X_train: pd.DataFrame, y_train: pd.Series, adaboost_params: dict) -> pd.DataFrame:
    """
    AdaBoost
    Strengths:
        Combines multiple weak learners to create a strong classifier.
        Focuses on examples that are hard to classify, improving overall performance.
    Recommended Use: 
        Can be effective for boosting weak classifiers in a genomics context.
    Fit AdaBoost classifier and return sorted feature importances.
    Recommended Use: Great for classification problems with a large number of features (genes).
    """
    ada = AdaBoostClassifier(**adaboost_params)
    ada.fit(X_train, y_train)
    return pd.DataFrame({"feature": X_train.columns, "importance": ada.feature_importances_}).sort_values(by="importance", ascending=False)

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
from skorch import NeuralNetClassifier  # sklearn compatible

class DNNClassifier(nn.Module):
    def __init__(self, input_dim, hidden_dim=128, output_dim=2, dropout_rate=0.5):
        super(DNNClassifier, self).__init__()
        
        self.hidden_layer1 = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Dropout(dropout_rate),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU()
        )
        
        self.hidden_layer2 = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Dropout(dropout_rate)
        )
        
        # Adding a residual connection between hidden layers
        self.residual = nn.Linear(input_dim, hidden_dim)
        
        self.output_layer = nn.Sequential(
            nn.Linear(hidden_dim, output_dim),
            nn.Softmax(dim=1)
        )
        
    def forward(self, x):
        residual = self.residual(x)
        x = self.hidden_layer1(x)
        x = x + residual  # Residual connection
        x = self.hidden_layer2(x)
        x = self.output_layer(x)
        return x

def validate_classifier(clf, X_train: pd.DataFrame, y_train: pd.Series, X_test: pd.DataFrame, y_test: pd.Series, metrics: list=["accuracy", "precision", "recall", "f1", "roc_auc"] , cv_folds: int=5) -> dict:
    """
    Perform cross-validation for a given classifier and return average scores for specified metrics on training data.
    Then fit the best model on the full training data and evaluate it on the test set.
    
    Parameters:
    - clf: The classifier to be validated.
    - X_train: Training features.
    - y_train: Training labels.
    - X_test: Test features.
    - y_test: Test labels.
    - metrics: List of metrics to evaluate (e.g., ['accuracy', 'roc_auc']).
    - cv_folds: Number of cross-validation folds.
    
    Returns:
    - results: Dictionary containing average cv_train_scores and cv_test_scores.
    """
    cv_train_scores = {metric: [] for metric in metrics}
    skf = StratifiedKFold(n_splits=cv_folds)
    # Perform cross-validation 
    for metric in metrics:
        try:
            if metric == "roc_auc" and len(set(y_train)) == 2:
                scores = cross_val_score(clf, X_train, y_train, cv=skf, scoring="roc_auc")
                cv_train_scores[metric] = np.nanmean(scores) if not np.isnan(scores).all() else float('nan')
            else:
                score = cross_val_score(clf, X_train, y_train, cv=skf, scoring=metric)
                cv_train_scores[metric] = score.mean()
        except Exception as e:
            cv_train_scores[metric] = float('nan')
    clf.fit(X_train, y_train)
    
    # Evaluate on the test set
    cv_test_scores = {}
    for metric in metrics:
        if metric == "roc_auc" and len(set(y_test)) == 2:
            try:
                y_prob=clf.predict_proba(X_test)[:, 1]
                cv_test_scores[metric] = roc_auc_score(y_test,y_prob)
            except AttributeError:
                cv_test_scores[metric]=float('nan')
        else:
            score_func = globals().get(f'{metric}_score')  # Fetching the appropriate scoring function
            if score_func:
                try:
                    y_pred = clf.predict(X_test)
                    cv_test_scores[metric] = score_func(y_test, y_pred)
                except Exception as e:
                    cv_test_scores[metric] = float('nan')

    # Combine results
    results = {
        'cv_train_scores': cv_train_scores,
        'cv_test_scores': cv_test_scores
    }
    return results

def get_classifiers(
    random_state=1,
    cls=[
        "lasso",
        "ridge",
        "Elastic Net(Enet)",
        "gradient Boosting",
        "Random forest (rf)",
        "XGBoost (xgb)",
        "Support Vector Machine(svm)",
        "naive bayes",
        "Linear Discriminant Analysis (lda)",
        "adaboost","DecisionTree","KNeighbors","Bagging"
    ],
):
    from sklearn.ensemble import (
        RandomForestClassifier,
        GradientBoostingClassifier,
        AdaBoostClassifier,
        BaggingClassifier
    )
    from sklearn.svm import SVC
    from sklearn.linear_model import LogisticRegression, Lasso, RidgeClassifierCV, ElasticNet
    from sklearn.naive_bayes import GaussianNB
    from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
    import xgboost as xgb
    from sklearn.tree import DecisionTreeClassifier
    from sklearn.neighbors import KNeighborsClassifier
    res_cls = {}
    classifiers_all = {
        "Lasso": LogisticRegression(penalty='l1', solver='saga', random_state=random_state),
        "Ridge": RidgeClassifierCV(),
        "Elastic Net (Enet)": ElasticNet(random_state=random_state),
        "Gradient Boosting": GradientBoostingClassifier(random_state=random_state),
        "Random Forest (RF)": RandomForestClassifier(random_state=random_state),
        "XGBoost (XGB)": xgb.XGBClassifier(random_state=random_state),
        "Support Vector Machine (SVM)": SVC(kernel="rbf", probability=True),
        "Naive Bayes": GaussianNB(),
        "Linear Discriminant Analysis (LDA)": LinearDiscriminantAnalysis(),
        "AdaBoost": AdaBoostClassifier(random_state=random_state, algorithm="SAMME"),
        "DecisionTree":DecisionTreeClassifier(),
        "KNeighbors": KNeighborsClassifier(n_neighbors=5),
        "Bagging": BaggingClassifier(),
    }
    print("Using default classifiers:")
    for cls_name in cls:
        cls_name = ips.strcmp(cls_name, list(classifiers_all.keys()))[0]
        res_cls[cls_name] = classifiers_all[cls_name]
        print(f"- {cls_name}")
    return res_cls

def get_features(
    X: pd.DataFrame,
    y: pd.Series,
    test_size: float = 0.2,
    random_state: int = 1,
    n_features: int = 10,
    rf_params: Optional[Dict] = None,
    rfe_params: Optional[Dict] = None,
    lasso_params: Optional[Dict] = None,
    ridge_params: Optional[Dict] = None,
    enet_params: Optional[Dict] = None,
    gb_params: Optional[Dict] = None,
    adaboost_params: Optional[Dict] = None,
    xgb_params: Optional[Dict] = None,
    dt_params: Optional[Dict] = None,
    bagging_params: Optional[Dict] = None,
    knn_params: Optional[Dict] = None,
    cls: list=[
        "lasso",
        "ridge",
        "Elastic Net(Enet)",
        "gradient Boosting",
        "Random forest (rf)",
        "XGBoost (xgb)",
        "Support Vector Machine(svm)",
        "naive bayes",
        "Linear Discriminant Analysis (lda)",
        "adaboost","DecisionTree","KNeighbors","Bagging"
    ],
    metrics: Optional[List[str]] = None,
    cv_folds: int = 5,
    strict:bool=False,
    n_shared:int=2, # 只要有两个方法有重合,就纳入common genes
    use_selected_features: bool = True,
) -> dict:
    """
    Master function to perform feature selection and validate classifiers.
    """
    # Split data into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )
    # Standardize features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Convert back to DataFrame for consistency
    X_train = pd.DataFrame(X_train_scaled, columns=X_train.columns)
    X_test = pd.DataFrame(X_test_scaled, columns=X_test.columns)

    rf_defaults = {"n_estimators": 100, "random_state": random_state}
    rfe_defaults = {"kernel": "linear", "n_features_to_select": n_features}
    lasso_defaults = {"alphas": np.logspace(-4, 4, 100), "cv": 10}
    ridge_defaults = {"alphas": np.logspace(-4, 4, 100), "cv": 10}
    enet_defaults = {"alphas": np.logspace(-4, 4, 100), "cv": 10}
    xgb_defaults = {"n_estimators": 100, "use_label_encoder": False, "eval_metric": "logloss", "random_state": random_state}
    gb_defaults = {"n_estimators": 100, "random_state": random_state}
    adaboost_defaults = {"n_estimators": 50, "random_state": random_state}
    dt_defaults = {"max_depth": None, "random_state": random_state}
    bagging_defaults = {"n_estimators": 50, "random_state": random_state}
    knn_defaults = {"n_neighbors": 5}
    rf_params, rfe_params = rf_params or rf_defaults, rfe_params or rfe_defaults
    lasso_params, ridge_params = lasso_params or lasso_defaults, ridge_params or ridge_defaults
    enet_params, xgb_params = enet_params or enet_defaults, xgb_params or xgb_defaults
    gb_params, adaboost_params = gb_params or gb_defaults, adaboost_params or adaboost_defaults
    dt_params = dt_params or dt_defaults
    bagging_params = bagging_params or bagging_defaults
    knn_params = knn_params or knn_defaults

    cls_  = ["lasso",'ridge','Elastic Net(Enet)',"Gradient Boosting","Random Forest (rf)",
             'XGBoost (xgb)','Support Vector Machine(svm)','Naive Bayes','Linear Discriminant Analysis (lda)','adaboost']
    cls=[ips.strcmp(i,cls_)[0] for i in cls]

    # Lasso Feature Selection
    lasso_importances = features_lasso(X_train, y_train, lasso_params) if 'lasso'in cls else pd.DataFrame()
    lasso_selected_features= lasso_importances.head(n_features)["feature"].values if 'lasso'in cls else []
    # Ridge 
    ridge_importances=features_ridge(X_train, y_train,ridge_params) if 'ridge'in cls else pd.DataFrame()
    selected_ridge_features= ridge_importances.head(n_features)["feature"].values if 'ridge'in cls else []
    # Elastic Net
    enet_importances=features_enet(X_train, y_train,enet_params) if 'Enet'in cls else pd.DataFrame()
    selected_enet_features= enet_importances.head(n_features)["feature"].values if 'Enet'in cls else []
    # Random Forest Feature Importance 
    rf_importances = features_rf(X_train, y_train, rf_params)  if 'Random Forest'in cls else pd.DataFrame()
    top_rf_features = rf_importances.head(n_features)["feature"].values if 'Random Forest'in cls else []
    # Gradient Boosting Feature Importance 
    gb_importances = features_gradient_boosting(X_train, y_train, gb_params) if 'Gradient Boosting'in cls else pd.DataFrame()
    top_gb_features = gb_importances.head(n_features)["feature"].values if 'Gradient Boosting'in cls else []
    # xgb
    xgb_importances = features_xgb(X_train, y_train,xgb_params) if 'xgb'in cls else pd.DataFrame()
    top_xgb_features = xgb_importances.head(n_features)["feature"].values if 'xgb'in cls else []
    
    # SVM with RFE 
    selected_svm_features = features_svm(X_train, y_train, rfe_params) if 'svm'in cls else []
    # Naive Bayes
    selected_naive_bayes_features=features_naive_bayes(X_train, y_train) if 'Naive Bayes'in cls else []
    # lda: linear discriminant analysis
    lda_importances=features_lda(X_train, y_train) if 'lda'in cls else pd.DataFrame()
    selected_lda_features= lda_importances.head(n_features)["feature"].values if 'lda'in cls else []
    # AdaBoost Feature Importance 
    adaboost_importances = features_adaboost(X_train, y_train, adaboost_params) if 'AdaBoost'in cls else pd.DataFrame()
    top_adaboost_features = adaboost_importances.head(n_features)["feature"].values if 'AdaBoost'in cls else []
    # Decision Tree Feature Importance
    dt_importances = features_decision_tree(X_train, y_train, dt_params) if 'Decision Tree' in cls else pd.DataFrame()
    top_dt_features = dt_importances.head(n_features)["feature"].values if 'Decision Tree' in cls else []
    # Bagging Feature Importance
    bagging_importances = features_bagging(X_train, y_train, bagging_params) if 'Bagging' in cls else pd.DataFrame()
    top_bagging_features = bagging_importances.head(n_features)["feature"].values if 'Bagging' in cls else []
    # KNN Feature Importance via Permutation
    knn_importances = features_knn(X_train, y_train, knn_params) if 'KNN' in cls else pd.DataFrame()
    top_knn_features = knn_importances.head(n_features)["feature"].values if 'KNN' in cls else []

    #! Find common features
    common_features = ips.shared(lasso_selected_features,selected_ridge_features, selected_enet_features,
                                 top_rf_features,top_gb_features,top_xgb_features,
                                 selected_svm_features, selected_naive_bayes_features,selected_lda_features,
                                 top_adaboost_features,top_dt_features, top_bagging_features, top_knn_features,
                                 strict=strict,
                                 n_shared=n_shared
                                 )

    # Use selected features or all features for model validation
    X_train_selected = X_train[list(common_features)] if use_selected_features else X_train
    X_test_selected = X_test[list(common_features)] if use_selected_features else X_test

    if metrics is None:
        metrics = ["accuracy", "precision", "recall", "f1", "roc_auc"] 

    # Prepare results DataFrame for selected features
    features_df = pd.DataFrame({
        'type': 
                ['Lasso'] * len(lasso_selected_features)+
                ['Ridge'] * len(selected_ridge_features)+
                ['Random Forest'] * len(top_rf_features) + 
                ['Gradient Boosting'] * len(top_gb_features)+
                ["Enet"]*len(selected_enet_features)+
                ['xgb'] * len(top_xgb_features)+
                ['SVM'] * len(selected_svm_features) + 
                ['Naive Bayes'] * len(selected_naive_bayes_features)+
                ['Linear Discriminant Analysis'] * len(selected_lda_features)+
                ['AdaBoost'] * len(top_adaboost_features)+
                ['Decision Tree'] * len(top_dt_features) + 
                ['Bagging'] * len(top_bagging_features) +
                ['KNN'] * len(top_knn_features),
        'feature': np.concatenate([lasso_selected_features,selected_ridge_features,
                                    top_rf_features,top_gb_features,selected_enet_features,top_xgb_features,
                                    selected_svm_features,selected_naive_bayes_features,
                                    selected_lda_features,top_adaboost_features,top_dt_features, 
                                    top_bagging_features, top_knn_features
                                    ])
    })

    #! Validate trained each classifier
    classifiers=get_classifiers(random_state=random_state,cls=cls) 
    cv_train_results,cv_test_results = [],[]
    for name, clf in classifiers.items():
        if not X_train_selected.empty:
            cv_scores=validate_classifier(clf, 
                                          X_train_selected, 
                                          y_train, 
                                          X_test_selected, 
                                          y_test, 
                                          metrics=metrics,
                                          cv_folds=cv_folds)

            cv_train_score_df = pd.DataFrame(cv_scores["cv_train_scores"], index=[name])
            cv_test_score_df = pd.DataFrame(cv_scores["cv_test_scores"], index=[name])
            cv_train_results.append(cv_train_score_df)
            cv_test_results.append(cv_test_score_df)
    if all([cv_train_results,cv_train_results]):
        cv_train_results_df = pd.concat(cv_train_results).reset_index().rename(columns={'index': 'Classifier'})
        cv_test_results_df = pd.concat(cv_test_results).reset_index().rename(columns={'index': 'Classifier'})
        #! Store results in the main results dictionary
        results = {
            "selected_features": features_df,
            "cv_train_scores": cv_train_results_df,
            "cv_test_scores": cv_test_results_df,
            "common_features": list(common_features),
        }
    else:
        results = {
            "selected_features": pd.DataFrame(),
            "cv_train_scores": pd.DataFrame(),
            "cv_test_scores": pd.DataFrame(),
            "common_features": [],
        }
        print(f"Warning: 没有找到共同的genes, when n_shared={n_shared}")
    return results
#! # usage:
# # Get features and common features
# results = get_features(X, y)
# common_features = results["common_features"]
def validate_features(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    X_true: pd.DataFrame,
    y_true: pd.Series,
    common_features:set=None,
    classifiers: Optional[Dict[str, Any]] = None,
    metrics: Optional[list] = None,
    random_state: int = 1,
    smote: bool = False,
    plot_: bool = True,
    class_weight: str = "balanced",
) -> dict:
    """
    Validate classifiers using selected features on the validation dataset.

    Parameters:
    - X_train (pd.DataFrame): Training feature dataset.
    - y_train (pd.Series): Training target variable.
    - X_true (pd.DataFrame): Validation feature dataset.
    - y_true (pd.Series): Validation target variable.
    - common_features (set): Set of common features to use for validation.
    - classifiers (dict, optional): Dictionary of classifiers to validate.
    - metrics (list, optional): List of metrics to compute.
    - random_state (int): Random state for reproducibility.
    - plot_ (bool): Option to plot metrics (to be implemented if needed).
    - class_weight (str or dict): Class weights to handle imbalance.

    """

    # Ensure common features are selected
    common_features = ips.shared(common_features, 
                                 X_train.columns, 
                                 X_true.columns,
                                 strict=True)

    # Filter the training and validation datasets for the common features
    X_train_selected = X_train[common_features]
    X_true_selected = X_true[common_features]

    if not X_true_selected.index.equals(y_true.index):
        raise ValueError("Index mismatch between validation features and target. Ensure data alignment.")
    
    y_true= y_true.loc[X_true_selected.index]

    # Handle class imbalance using SMOTE
    if smote:
        if y_train.value_counts(normalize=True).max() < 0.8:  # Threshold to decide if data is imbalanced
            smote = SMOTE(random_state=random_state)
            X_train_resampled, y_train_resampled = smote.fit_resample(
                X_train_selected, y_train
            )
        else:
            # skip SMOTE
            X_train_resampled, y_train_resampled = X_train_selected, y_train
    else:
        X_train_resampled, y_train_resampled = X_train_selected, y_train

    # Default classifiers if not provided
    if classifiers is None:
        classifiers = {
            "Random Forest": RandomForestClassifier(
                class_weight=class_weight, random_state=random_state
            ),
            "SVM": SVC(probability=True, class_weight=class_weight),
            "Logistic Regression": LogisticRegression(
                class_weight=class_weight, random_state=random_state
            ),
            "Gradient Boosting": GradientBoostingClassifier(random_state=random_state),
            "AdaBoost": AdaBoostClassifier(random_state=random_state, algorithm="SAMME"),
            "Lasso": LogisticRegression(penalty='l1', solver='saga', random_state=random_state),
            "Ridge": LogisticRegression(penalty='l2', solver='saga', random_state=random_state),
            "Elastic Net": LogisticRegression(penalty='elasticnet', solver='saga', l1_ratio=0.5, random_state=random_state),
            "XGBoost": xgb.XGBClassifier(use_label_encoder=False, eval_metric='logloss'),
            "Naive Bayes": GaussianNB(),
            "LDA": LinearDiscriminantAnalysis()
        }

    # Hyperparameter grids for tuning 
    param_grids = {
        "Random Forest": {
            'n_estimators': [100, 200, 300, 400, 500],
            'max_depth': [None, 3, 5, 10, 20],
            'min_samples_split': [2, 5, 10],
            'min_samples_leaf': [1, 2, 4],
            'class_weight': [None, 'balanced']
        },
        "SVM": {
            'C': [0.01, 0.1, 1, 10, 100, 1000],
            'gamma': [0.001, 0.01, 0.1, 'scale', 'auto'],
            'kernel': ['linear', 'rbf', 'poly']
        },
        "Logistic Regression": {
            'C': [0.01, 0.1, 1, 10, 100],
            'solver': ['liblinear', 'saga', 'newton-cg', 'lbfgs'],
            'penalty': ['l1', 'l2'],
            'max_iter': [100, 200, 300]
        },
        "Gradient Boosting": {
            'n_estimators': [100, 200, 300, 400, 500],
            'learning_rate': np.logspace(-3, 0, 4),
            'max_depth': [3, 5, 7, 9],
            'min_samples_split': [2, 5, 10]
        },
        "AdaBoost": {
            'n_estimators': [50, 100, 200, 300, 500],
            'learning_rate': np.logspace(-3, 0, 4)
        },
        "Lasso": {
            'C': np.logspace(-3, 1, 10),
            'max_iter': [100, 200, 300]
        },
        "Ridge": {
            'C': np.logspace(-3, 1, 10),
            'max_iter': [100, 200, 300]
        },
        "Elastic Net": {
            'C': np.logspace(-3, 1, 10),
            'l1_ratio': [0.1, 0.5, 0.9],
            'max_iter': [100, 200, 300]
        },
        "XGBoost": {
            'n_estimators': [100, 200],
            'max_depth': [3, 5, 7],
            'learning_rate': [0.01, 0.1, 0.2],
            'subsample': [0.8, 1.0],
            'colsample_bytree': [0.8, 1.0]
        },
        "Naive Bayes": {},
        "LDA": {
            'solver': ['svd', 'lsqr', 'eigen']
        }
    }
    # Default metrics if not provided
    if metrics is None:
        metrics = ["accuracy", "precision", "recall", "f1", "roc_auc", "mcc", "specificity", "balanced_accuracy", "pr_auc"]

    results = {}

    # Validate each classifier with GridSearchCV
    for name, clf in classifiers.items():
        print(f"\nValidating {name} on the validation dataset:")

        # Check if `predict_proba` method exists; if not, use CalibratedClassifierCV
        # 没有predict_proba的分类器，使用 CalibratedClassifierCV 可以获得校准的概率估计。此外，为了使代码更灵活，我们可以在创建分类器
        # 时检查 predict_proba 方法是否存在，如果不存在且用户希望计算 roc_auc 或 pr_auc，则启用 CalibratedClassifierCV
        if not hasattr(clf, "predict_proba"):
            print(f"Using CalibratedClassifierCV for {name} due to lack of probability estimates.")
            calibrated_clf = CalibratedClassifierCV(clf, method='sigmoid', cv='prefit')
        else:
            calibrated_clf = clf
        # Stratified K-Fold for cross-validation
        skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=random_state)

        # Create GridSearchCV object
        gs = GridSearchCV(
            estimator=  calibrated_clf,
            param_grid=param_grids[name],
            scoring="roc_auc",  # Optimize for ROC AUC
            cv=skf,  # Stratified K-Folds cross-validation
            n_jobs=-1, 
            verbose=1,
        )

        # Fit the model using GridSearchCV
        gs.fit(X_train_resampled, y_train_resampled)
        # Best estimator from grid search
        best_clf = gs.best_estimator_
        # Make predictions on the validation set
        y_pred = best_clf.predict(X_true_selected)
        # Calculate probabilities for ROC AUC if possible
        if hasattr(best_clf, "predict_proba"):
            y_pred_proba = best_clf.predict_proba(X_true_selected)[:, 1]
        elif hasattr(best_clf, "decision_function"):
            # If predict_proba is not available, use decision_function (e.g., for SVM)
            y_pred_proba = best_clf.decision_function(X_true_selected)
            # Ensure y_pred_proba is within 0 and 1 bounds
            y_pred_proba = (y_pred_proba - y_pred_proba.min()) / (y_pred_proba.max() - y_pred_proba.min())
        else:
            y_pred_proba = None  # No probability output for certain models

        # Calculate metrics
        validation_scores = {}
        for metric in metrics:
            if metric == "accuracy":
                validation_scores[metric] = accuracy_score(y_true, y_pred)
            elif metric == "precision":
                validation_scores[metric] = precision_score(y_true, y_pred, average='weighted')
            elif metric == "recall":
                validation_scores[metric] = recall_score(y_true, y_pred, average='weighted')
            elif metric == "f1":
                validation_scores[metric] = f1_score(y_true, y_pred, average='weighted')
            elif metric == "roc_auc" and y_pred_proba is not None:
                validation_scores[metric] = roc_auc_score(y_true, y_pred_proba)
            elif metric == "mcc":
                validation_scores[metric] = matthews_corrcoef(y_true, y_pred)
            elif metric == "specificity":
                tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
                validation_scores[metric] = tn / (tn + fp)  # Specificity calculation
            elif metric == "balanced_accuracy":
                validation_scores[metric] = balanced_accuracy_score(y_true, y_pred)
            elif metric == "pr_auc"  and y_pred_proba is not None:
                precision, recall, _ = precision_recall_curve(y_true, y_pred_proba)
                validation_scores[metric] = average_precision_score(y_true, y_pred_proba)
    
        # Calculate ROC curve
        #https://scikit-learn.org/stable/auto_examples/model_selection/plot_roc.html
        if y_pred_proba is not None:
            # fpr, tpr, roc_auc = dict(), dict(), dict()
            fpr, tpr, _ = roc_curve(y_true, y_pred_proba)
            lower_ci, upper_ci = cal_auc_ci(y_true, y_pred_proba)
            roc_auc=auc(fpr, tpr)
            roc_info={
                "fpr": fpr.tolist(),
                "tpr": tpr.tolist(),
                "auc":roc_auc,
                "ci95":(lower_ci, upper_ci)
            }
            # precision-recall curve
            precision_, recall_, _  = precision_recall_curve(y_true, y_pred_proba)
            avg_precision_ = average_precision_score(y_true, y_pred_proba)
            pr_info = {"precision": precision_,
                       "recall":recall_,
                       "avg_precision":avg_precision_
                       }
        else:
            roc_info,pr_info=None,None
        results[name] = {
            "best_params": gs.best_params_,
            "scores": validation_scores,
            "roc_curve": roc_info,
            "pr_curve": pr_info,
            "confusion_matrix": confusion_matrix(y_true, y_pred),
        }
 
    df_results = pd.DataFrame.from_dict(results, orient="index")

    return df_results

 #! usage validate_features()
 # Validate classifiers using the validation dataset (X_val, y_val)
# validation_results = validate_features(X, y, X_val, y_val, common_features)

# # If you want to access validation scores
# print(validation_results)
 
 
def cal_auc_ci(y_true, y_pred, n_bootstraps=1000, ci=0.95,random_state=1):
    y_true = np.asarray(y_true)
    y_pred = np.asarray(y_pred)
    bootstrapped_scores = []
    print("auroc score:", roc_auc_score(y_true, y_pred))
    rng = np.random.RandomState(random_state)
    for i in range(n_bootstraps):
        # bootstrap by sampling with replacement on the prediction indices
        indices = rng.randint(0, len(y_pred), len(y_pred))
        if len(np.unique(y_true[indices])) < 2:
            # We need at least one positive and one negative sample for ROC AUC
            # to be defined: reject the sample
            continue
        if isinstance(y_true, np.ndarray):
            score = roc_auc_score(y_true[indices], y_pred[indices])
        else:
            score = roc_auc_score(y_true.iloc[indices], y_pred.iloc[indices])
        bootstrapped_scores.append(score)
        # print("Bootstrap #{} ROC area: {:0.3f}".format(i + 1, score))
    sorted_scores = np.array(bootstrapped_scores)
    sorted_scores.sort()

    # Computing the lower and upper bound of the 90% confidence interval
    # You can change the bounds percentiles to 0.025 and 0.975 to get
    # a 95% confidence interval instead.
    confidence_lower = sorted_scores[int((1-ci) * len(sorted_scores))]
    confidence_upper = sorted_scores[int(ci * len(sorted_scores))]
    print(
        "Confidence interval for the score: [{:0.3f} - {:0.3}]".format(
            confidence_lower, confidence_upper
        )
    )
    return confidence_lower, confidence_upper

def plot_roc_curve(
    fpr=None,
    tpr=None,
    mean_auc=None,
    lower_ci=None,
    upper_ci=None,
    color="#FF8F00",
    lw=2,
    alpha=0.1,
    ci_display=True,
    title="ROC Curve",
    xlabel="1−Specificity",
    ylabel="Sensitivity",
    legend_loc="lower right",
    diagonal_color="0.5",
    figsize=(5, 5),
    ax=None,
    **kwargs
):
    if ax is None:
        fig, ax = plt.subplots(figsize=figsize)
    if mean_auc is not None:
        if ci_display:
            label = (
                f"ROC curve (AUC = {mean_auc:.3f})\n95% CI: {lower_ci:.3f} - {upper_ci:.3f}"
            )
        else:
            label = f"ROC curve (AUC = {mean_auc:.3f})"
    else:
        label = None

    # Plot ROC curve and the diagonal reference line
    ax.fill_between(fpr, tpr, alpha=alpha, color=color)
    ax.plot([0, 1], [0, 1], color=diagonal_color, linestyle="--")
    ax.plot(fpr, tpr, color=color, lw=lw, label=label,**kwargs)
    # Setting plot limits, labels, and title
    ax.set_xlim([-0.01, 1.0])
    ax.set_ylim([0.0, 1.0])
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.legend(loc=legend_loc)
    return ax
#* usage: ml2ls.plot_roc_curve(fpr, tpr, mean_auc, lower_ci, upper_ci)
# for model_name in flatten(validation_results["roc_curve"].keys())[2:]:
#     fpr = validation_results["roc_curve"][model_name]["fpr"]
#     tpr = validation_results["roc_curve"][model_name]["tpr"]
#     (lower_ci, upper_ci) = validation_results["roc_curve"][model_name]["ci95"]
#     mean_auc = validation_results["roc_curve"][model_name]["auc"]

#     # Plotting
#     ml2ls.plot_roc_curve(fpr, tpr, mean_auc, lower_ci, upper_ci)
#     figsets(title=model_name)

def plot_pr_curve(
    recall=None,
    precision=None,
    avg_precision=None,
    model_name=None,
    lw=2,
    figsize=[5, 5],
    title="Precision-Recall Curve",
    xlabel="Recall",
    ylabel="Precision",
    alpha=0.1,
    color="#FF8F00", 
    legend_loc="lower left",
    ax=None,
    **kwargs
):
    if ax is None:
        fig, ax = plt.subplots(figsize=figsize)

    # Plot Precision-Recall curve
    ax.plot(recall,
            precision,
            lw=lw,
            color=color,
            label=( f"PR curve (AUC={avg_precision:.2f})"),
            **kwargs)
    # Fill area under the curve
    ax.fill_between(recall, precision, alpha=alpha, color=color)

    # Customize axes
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_xlim([-0.01, 1.0])
    ax.set_ylim([0.0, 1.0])
    ax.grid(False) 
    ax.legend(loc=legend_loc)
    return ax
#* usage: ml2ls.plot_pr_curve()
# for md_name in flatten(validation_results["pr_curve"].keys()):
#     ml2ls.plot_pr_curve(
#         recall=validation_results["pr_curve"][md_name]["recall"],
#         precision=validation_results["pr_curve"][md_name]["precision"],
#         avg_precision=validation_results["pr_curve"][md_name]["avg_precision"],
#         model_name=md_name,
#         lw=2,
#         alpha=0.1,
#         color="r",
#     )

def plot_cm(
    cm,
    labels_name=None,
    thresh=0.8,
    axis_labels=None,
    cmap="Reds",
    normalize=True,
    xlabel="Predicted Label",
    ylabel="Actual Label",
    fontsize=12,
    figsize=[5, 5],
    ax=None,
):
    if ax is None:
        fig, ax = plt.subplots(figsize=figsize)

    cm_normalized = np.round(cm.astype("float") / cm.sum(axis=1)[:, np.newaxis] * 100, 2)
    cm_value = cm_normalized if normalize else cm.astype("int")
    # Plot the heatmap
    cax = ax.imshow(cm_normalized, interpolation="nearest", cmap=cmap)
    plt.colorbar(cax, ax=ax, fraction=0.046, pad=0.04)
    cax.set_clim(0, 100)

    # Define tick labels based on provided labels
    num_local = np.arange(len(labels_name)) if labels_name is not None else range(2)
    if axis_labels is None:
        axis_labels = labels_name if labels_name is not None else ["No","Yes"]
    ax.set_xticks(num_local)
    ax.set_xticklabels(axis_labels)
    ax.set_yticks(num_local)
    ax.set_yticklabels(axis_labels)
    ax.set_ylabel(ylabel)
    ax.set_xlabel(xlabel)
    plot.figsets(ax=ax, xtickloc="tl", boxloc="none")

    # Add TN, FP, FN, TP annotations specifically for binary classification (2x2 matrix)
    if labels_name is None or len(labels_name) == 2:
        # True Negative (TN), False Positive (FP), False Negative (FN), and True Positive (TP)
        #                 Predicted
        #                0   |   1
        #             ----------------
        #         0 |   TN   |  FP
        # Actual      ----------------
        #         1 |   FN   |  TP
        tn_label = "TN"
        fp_label = "FP"
        fn_label = "FN"
        tp_label = "TP"

        # Adjust positions slightly for TN, FP, FN, TP labels
        ax.text(0,0,
            f"{tn_label}:{cm_normalized[0, 0]:.2f}%" if normalize else f"{tn_label}:{cm_value[0, 0]}",
            ha="center",
            va="center",
            color="white" if cm_normalized[0, 0] > thresh * 100 else "black",
            fontsize=fontsize,
        )
        ax.text(1,0,
            f"{fp_label}:{cm_normalized[0, 1]:.2f}%" if normalize else f"{tn_label}:{cm_value[0, 1]}",
            ha="center",
            va="center",
            color="white" if cm_normalized[0, 1] > thresh * 100 else "black",
            fontsize=fontsize,
        )
        ax.text(0,1,
            f"{fn_label}:{cm_normalized[1, 0]:.2f}%" if normalize else f"{tn_label}:{cm_value[1, 0]}",
            ha="center",
            va="center",
            color="white" if cm_normalized[1, 0] > thresh * 100 else "black",
            fontsize=fontsize,
        )
        ax.text(1,1,
            f"{tp_label}:{cm_normalized[1, 1]:.2f}%" if normalize else f"{tn_label}:{cm_value[1, 1]}",
            ha="center",
            va="center",
            color="white" if cm_normalized[1, 1] > thresh * 100 else "black",
            fontsize=fontsize,
        )
    else:
        # Annotate cells with normalized percentage values
        for i in range(len(labels_name)):
            for j in range(len(labels_name)):
                val = cm_normalized[i, j]
                color = "white" if val > thresh * 100 else "black"
                ax.text(j,i,
                    f"{val:.2f}%",
                    ha="center",
                    va="center",
                    color=color,
                    fontsize=fontsize,
                )
    return ax
