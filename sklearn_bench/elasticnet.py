# ===============================================================================
# Copyright 2020-2021 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ===============================================================================

import argparse

import bench


def main():
    from sklearn.linear_model import ElasticNet

    # Load data
    X_train, X_test, y_train, y_test = bench.load_data(params)

    # Create our regression object
    regr = ElasticNet(fit_intercept=params.fit_intercept, l1_ratio=params.l1_ratio,
                      alpha=params.alpha, tol=params.tol,
                      max_iter=params.maxiter, copy_X=False)
    # Time fit
    fit_time, _ = bench.measure_function_time(regr.fit, X_train, y_train, params=params)

    # Time predict
    predict_time, y_pred = bench.measure_function_time(regr.predict,
                                                       X_train, params=params)

    train_rmse = bench.rmse_score(y_train, y_pred)
    train_r2 = bench.r2_score(y_train, y_pred)
    y_pred = regr.predict(X_test)
    test_rmse = bench.rmse_score(y_test, y_pred)
    test_r2 = bench.r2_score(y_test, y_pred)

    bench.print_output(
        library='sklearn',
        algorithm='elasticnet',
        stages=['training', 'prediction'],
        params=params,
        functions=['ElasticNet.fit', 'ElasticNet.predict'],
        times=[fit_time, predict_time],
        metric_type=['rmse', 'r2_score', 'iter'],
        metrics=[
            [train_rmse, test_rmse],
            [train_r2, test_r2],
            [int(regr.n_iter_), int(regr.n_iter_)],
        ],
        data=[X_train, X_train],
        alg_instance=regr,
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='scikit-learn elastic-net regression '
                                     'benchmark')
    parser.add_argument('--no-fit-intercept', dest='fit_intercept', default=False,
                        action='store_false',
                        help="Don't fit intercept (assume data already centered)")
    parser.add_argument('--alpha', dest='alpha', type=float, default=1.0,
                        help='Regularization parameter')
    parser.add_argument('--maxiter', type=int, default=1000,
                        help='Maximum iterations for the iterative solver')
    parser.add_argument('--l1_ratio', dest='l1_ratio', type=float, default=0.5,
                        help='Regularization parameter')
    parser.add_argument('--tol', type=float, default=0.0,
                        help='Tolerance for solver.')
    params = bench.parse_args(parser)
    bench.run_with_context(params, main)
