from sklearn.ensemble import GradientBoostingClassifier
from sklearn import datasets, model_selection
import numpy as np

if __name__ == '__main__':
    wdbc = datasets.load_breast_cancer()

    model = GradientBoostingClassifier(
        n_estimators=100,
        learning_rate=0.693,
        max_depth=3,
        min_samples_split=6,
        min_samples_leaf=1,
        max_features='sqrt',
        random_state=2
    )

    cv_results = model_selection.cross_validate(
        model, wdbc.data, wdbc.target, cv=5, return_train_score=True
    )

    acc_train = np.mean(cv_results['train_score'])
    acc_test = np.mean(cv_results['test_score'])
    print(f'* Accuracy @ training data: {acc_train:.3f}')
    print(f'* Accuracy @ test data: {acc_test:.3f}')
    print(f'* Your score: {max(10 + 100 * (acc_test - 0.9), 0):.0f}')