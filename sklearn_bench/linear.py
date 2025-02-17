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
    from sklearn.linear_model import LinearRegression

    # Load data
    X_train, X_test, y_train, y_test = bench.load_data(
        params, generated_data=['X_train', 'y_train'])

    # Create our regression object
    regr = LinearRegression(fit_intercept=params.fit_intercept,
                            n_jobs=params.n_jobs, copy_X=False)

    # Time fit
    fit_time, _ = bench.measure_function_time(regr.fit, X_train, y_train, params=params)

    # Time predict
    predict_time, yp = bench.measure_function_time(regr.predict, X_test, params=params)

    test_rmse = bench.rmse_score(y_test, yp)
    test_r2 = bench.r2_score(y_test, yp)
    yp = regr.predict(X_train)
    train_rmse = bench.rmse_score(y_train, yp)
    train_r2 = bench.r2_score(y_train, yp)

    bench.print_output(
        library='sklearn', algorithm='lin_reg',
        stages=['training', 'prediction'],
        params=params, functions=['Linear.fit', 'Linear.predict'],
        times=[fit_time, predict_time],
        metric_type=['rmse', 'r2_score'],
        metrics=[[train_rmse, test_rmse], [train_r2, test_r2]],
        data=[X_train, X_test],
        alg_instance=regr,
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='scikit-learn linear regression '
                                     'benchmark')
    parser.add_argument('--no-fit-intercept', dest='fit_intercept', default=True,
                        action='store_false',
                        help="Don't fit intercept (assume data already centered)")
    params = bench.parse_args(parser)
    bench.run_with_context(params, main)
