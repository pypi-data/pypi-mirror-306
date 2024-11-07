class AutoMLSearch:
    """Automated Pipeline search.

    Args:
        X_train (pd.DataFrame): The input training data of shape [n_samples, n_features]. Required.

        y_train (pd.Series): The target training data of length [n_samples]. Required for supervised learning tasks.

        X_holdout (pd.DataFrame): The input holdout data of shape [n_samples, n_features].

        y_holdout (pd.Series): The target holdout data of length [n_samples].

        problem_type (str or ProblemTypes): Type of supervised learning problem.

        objective (str, ObjectiveBase): The objective to optimize for. Used to propose and rank pipelines, but not for optimizing each pipeline during fit-time.
            When set to 'auto', chooses:
            - LogLossBinary for binary classification problems,
            - LogLossMulticlass for multiclass classification problems, and
            - R2 for regression problems.

        max_iterations (int): Maximum number of iterations to search. If max_iterations and
            max_time is not set, then max_iterations will default to max_iterations of 5.

        max_time (int, str): Maximum time to search for pipelines.
            This will not start a new pipeline search after the duration
            has elapsed. If it is an integer, then the time will be in seconds.
            For strings, time can be specified as seconds, minutes, or hours.

        patience (int): Number of iterations without improvement to stop search early. Must be positive.
            If None, early stopping is disabled. Defaults to None.

        tolerance (float): Minimum percentage difference to qualify as score improvement for early stopping.
            Only applicable if patience is not None. Defaults to None.

        allowed_component_graphs (dict): A dictionary of lists or ComponentGraphs indicating the component graphs allowed in the search.
            The format should follow { "Name_0": [list_of_components], "Name_1": ComponentGraph(...) }

            The default of None indicates all pipeline component graphs for this problem type are allowed. Setting this field will cause
            allowed_model_families to be ignored.

            e.g. allowed_component_graphs = { "My_Graph": ["Imputer", "One Hot Encoder", "Random Forest Classifier"] }

        allowed_model_families (list(str, ModelFamily)): The model families to search. The default of None searches over all
            model families. Change `binary` to `multiclass` or `regression` depending on the problem type. Note that if allowed_pipelines
            is provided, this parameter will be ignored.

        features (list)[FeatureBase]: List of features to run DFS on AutoML pipelines. Defaults to None.
            Features will only be computed if the columns used by the feature exist in the search input
            and if the feature itself is not in search input. If features is an empty list, the DFS Transformer will not be included in pipelines.

        data_splitter (sklearn.model_selection.BaseCrossValidator): Data splitting method to use. Defaults to StratifiedKFold.

        tuner_class: The tuner class to use. Defaults to SKOptTuner.

        optimize_thresholds (bool): Whether or not to optimize the binary pipeline threshold. Defaults to True.

        start_iteration_callback (callable): Function called before each pipeline training iteration.
            Callback function takes three positional parameters: The pipeline instance and the AutoMLSearch object.

        add_result_callback (callable): Function called after each pipeline training iteration.
            Callback function takes three positional parameters: A dictionary containing the training results for the new pipeline, an
            untrained_pipeline containing the parameters used during training, and the AutoMLSearch object.

        error_callback (callable): Function called when `search()` errors and raises an Exception.
            Callback function takes three positional parameters: the Exception raised, the traceback, and the AutoMLSearch object.
            Must also accepts kwargs, so AutoMLSearch is able to pass along other appropriate parameters by default.
            Defaults to None, which will call `log_error_callback`.

        additional_objectives (list): Custom set of objectives to score on.
            Will override default objectives for problem type if not empty.

        alternate_thresholding_objective (str): The objective to use for thresholding binary classification pipelines if the main objective provided isn't tuneable.
            Defaults to F1.

        random_seed (int): Seed for the random number generator. Defaults to 0.

        n_jobs (int or None): Non-negative integer describing level of parallelism used for pipelines.
            None and 1 are equivalent. If set to -1, all CPUs are used. For n_jobs below -1, (n_cpus + 1 + n_jobs) are used.

        ensembling (boolean): If True, runs ensembling in a separate batch after every allowed pipeline class has been iterated over.
            If the number of unique pipelines to search over per batch is one, ensembling will not run. Defaults to False.

        max_batches (int): The maximum number of batches of pipelines to search. Parameters max_time, and
            max_iterations have precedence over stopping the search.

        problem_configuration (dict, None): Additional parameters needed to configure the search. For example,
            in time series problems, values should be passed in for the time_index, gap, forecast_horizon, and max_delay variables.

        train_best_pipeline (boolean): Whether or not to train the best pipeline before returning it. Defaults to True.

        search_parameters (dict): A dict of the hyperparameter ranges or pipeline parameters used to iterate over during search.
            Keys should consist of the component names and values should specify a singular value/list for pipeline parameters, or skopt.Space for hyperparameter ranges.
            In the example below, the Imputer parameters would be passed to the hyperparameter ranges, and the Label Encoder parameters would be used as the component parameter.

            e.g. search_parameters = { 'Imputer' : { 'numeric_impute_strategy': Categorical(['most_frequent', 'median']) },
                                       'Label Encoder': {'positive_label': True} }

        sampler_method (str): The data sampling component to use in the pipelines if the problem type is classification and the target balance is smaller than the sampler_balanced_ratio.
            Either 'auto', which will use our preferred sampler for the data, 'Undersampler', 'Oversampler', or None. Defaults to 'auto'.

        sampler_balanced_ratio (float): The minority:majority class ratio that we consider balanced, so a 1:4 ratio would be equal to 0.25. If the class balance is larger than this provided value,
            then we will not add a sampler since the data is then considered balanced. Overrides the `sampler_ratio` of the samplers. Defaults to 0.25.

        allow_long_running_models (bool): Whether or not to allow longer-running models for large multiclass problems. If False and no pipelines, component graphs, or model families are provided,
            AutoMLSearch will not use Elastic Net or XGBoost when there are more than 75 multiclass targets and will not use CatBoost when there are more than 150 multiclass targets. Defaults to False.

        _ensembling_split_size (float): The amount of the training data we'll set aside for training ensemble metalearners. Only used when ensembling is True.
            Must be between 0 and 1, exclusive. Defaults to 0.2

        _pipelines_per_batch (int): The number of pipelines to train for every batch after the first one.
            The first batch will train a baseline pipline + one of each pipeline family allowed in the search.

        automl_algorithm (str): The automl algorithm to use. Currently the two choices are 'iterative' and 'default'. Defaults to `default`.

        engine (EngineBase or str): The engine instance used to evaluate pipelines. Dask or concurrent.futures engines can also
            be chosen by providing a string from the list ["sequential", "cf_threaded", "cf_process", "dask_threaded", "dask_process"].
            If a parallel engine is selected this way, the maximum amount of parallelism, as determined by the engine, will be used. Defaults to "sequential".

        verbose (boolean): Whether or not to display semi-real-time updates to stdout while search is running. Defaults to False.

        timing (boolean): Whether or not to write pipeline search times to the logger. Defaults to False.
        exclude_featurizers (list[str]): A list of featurizer components to exclude from the pipelines built by search.
            Valid options are "DatetimeFeaturizer", "EmailFeaturizer", "URLFeaturizer", "NaturalLanguageFeaturizer", "TimeSeriesFeaturizer"

        holdout_set_size (float): The size of the holdout set that AutoML search will take for datasets larger than 500 rows. If set to 0, holdout set will not be taken regardless of number of rows. Must be between 0 and 1, exclusive. Defaults to 0.1.
    """

    def __init__(
        self,
        X_train=None,
        y_train=None,
        X_holdout=None,
        y_holdout=None,
        problem_type=None,
        objective="auto",
        max_iterations=None,
        max_time=None,
        patience=None,
        tolerance=None,
        data_splitter=None,
        allowed_component_graphs=None,
        allowed_model_families=None,
        features=None,
        start_iteration_callback=None,
        add_result_callback=None,
        error_callback=None,
        additional_objectives=None,
        alternate_thresholding_objective="F1",
        random_seed=0,
        n_jobs=-1,
        tuner_class=None,
        optimize_thresholds=True,
        ensembling=False,
        max_batches=None,
        problem_configuration=None,
        train_best_pipeline=True,
        search_parameters=None,
        sampler_method="auto",
        sampler_balanced_ratio=0.25,
        allow_long_running_models=False,
        _pipelines_per_batch=5,
        automl_algorithm="default",
        engine="sequential",
        verbose=False,
        timing=False,
        exclude_featurizers=None,
        holdout_set_size=0,
        empty=False,
    ):
        from evalml.automl.automl_search import AutoMLSearch

        if not empty:
            self.__ = AutoMLSearch(
                X_train,
                y_train,
                X_holdout,
                y_holdout,
                problem_type,
                objective,
                max_iterations,
                max_time,
                patience,
                tolerance,
                data_splitter,
                allowed_component_graphs,
                allowed_model_families,
                features,
                start_iteration_callback,
                add_result_callback,
                error_callback,
                additional_objectives,
                alternate_thresholding_objective,
                random_seed,
                n_jobs,
                tuner_class,
                optimize_thresholds,
                ensembling,
                max_batches,
                problem_configuration,
                train_best_pipeline,
                search_parameters,
                sampler_method,
                sampler_balanced_ratio,
                allow_long_running_models,
                _pipelines_per_batch,
                automl_algorithm,
                engine,
                verbose,
                timing,
                exclude_featurizers,
                holdout_set_size,
            )

    def __str__(self):
        """Returns string representation of the AutoMLSearch object."""
        from evalml.objectives import get_objective
        from evalml.problem_types.utils import handle_problem_types

        def _print_list(obj_list):
            lines = sorted(["\t{}".format(o.name) for o in obj_list])
            return "\n".join(lines)

        def _get_funct_name(function):
            if callable(function):
                return function.__name__
            else:
                return None

        search_desc = (
            f"{handle_problem_types(self.problem_type).name} Search\n\n"
            f"Parameters: \n{'='*20}\n"
            f"Objective: {get_objective(self.objective).name}\n"
            f"Max Time: {self.max_time}\n"
            f"Max Iterations: {self.max_iterations}\n"
            f"Max Batches: {self.max_batches}\n"
            f"Allowed Pipelines: \n{_print_list(self.allowed_pipelines or [])}\n"
            f"Patience: {self.patience}\n"
            f"Tolerance: {self.tolerance}\n"
            f"Data Splitting: {self.data_splitter}\n"
            f"Tuner: {self.tuner_class.__name__}\n"
            f"Start Iteration Callback: {_get_funct_name(self.start_iteration_callback)}\n"
            f"Add Result Callback: {_get_funct_name(self.add_result_callback)}\n"
            f"Additional Objectives: {_print_list(self.additional_objectives or [])}\n"
            f"Random Seed: {self.random_seed}\n"
            f"n_jobs: {self.n_jobs}\n"
            f"Optimize Thresholds: {self.optimize_thresholds}\n"
        )

        rankings_desc = ""
        if not self.rankings.empty:
            rankings_str = self.rankings.drop(
                ["parameters"],
                axis="columns",
            ).to_string()
            rankings_desc = f"\nSearch Results: \n{'='*20}\n{rankings_str}"

        return search_desc + rankings_desc

    def close_engine(self):
        """Function to explicitly close the engine, client, parallel resources."""
        return self.__.close_engine()

    def search(self, interactive_plot=True):
        """Find the best pipeline for the data set.

        Args:
            interactive_plot (boolean, True): Shows an iteration vs. score plot in Jupyter notebook.
                Disabled by default in non-Jupyter enviroments.

        Raises:
            AutoMLSearchException: If all pipelines in the current AutoML batch produced a score of np.nan on the primary objective.

        Returns:
            Dict[int, Dict[str, Timestamp]]: Dictionary keyed by batch number that maps to the timings for pipelines run in that batch,
            as well as the total time for each batch. Pipelines within a batch are labeled by pipeline name.
        """
        return self.__.search(interactive_plot)

    def get_pipeline(self, pipeline_id):
        """Given the ID of a pipeline training result, returns an untrained instance of the specified pipeline initialized with the parameters used to train that pipeline during automl search.

        Args:
            pipeline_id (int): Pipeline to retrieve.

        Returns:
            PipelineBase: Untrained pipeline instance associated with the provided ID.

        Raises:
            PipelineNotFoundError: if pipeline_id is not a valid ID.
        """
        return self.__.get_pipeline(pipeline_id)

    def describe_pipeline(self, pipeline_id, return_dict=False):
        """Describe a pipeline.

        Args:
            pipeline_id (int): pipeline to describe
            return_dict (bool): If True, return dictionary of information
                about pipeline. Defaults to False.

        Returns:
            Description of specified pipeline. Includes information such as
            type of pipeline components, problem, training time, cross validation, etc.

        Raises:
            PipelineNotFoundError: If pipeline_id is not a valid ID.
        """
        return self.__.describe_pipeline(pipeline_id, return_dict)

    def add_to_rankings(self, pipeline):
        """Fits and evaluates a given pipeline then adds the results to the automl rankings with the requirement that automl search has been run.

        Args:
            pipeline (PipelineBase): pipeline to train and evaluate.
        """
        return self.__.add_to_rankings(pipeline)

    @property
    def results(self):
        """Class that allows access to a copy of the results from `automl_search`.

        Returns:
            dict: Dictionary containing `pipeline_results`, a dict with results from each pipeline,
                 and `search_order`, a list describing the order the pipelines were searched.
        """
        return self.__.results

    @property
    def rankings(self):
        """Returns a pandas.DataFrame with scoring results from the highest-scoring set of parameters used with each pipeline."""
        return self.__.rankings

    @property
    def full_rankings(self):
        """Returns a pandas.DataFrame with scoring results from all pipelines searched."""
        return self.__.full_rankings

    @property
    def best_pipeline(self):
        """Returns a trained instance of the best pipeline and parameters found during automl search. If `train_best_pipeline` is set to False, returns an untrained pipeline instance.

        Returns:
            PipelineBase: A trained instance of the best pipeline and parameters found during automl search. If `train_best_pipeline` is set to False, returns an untrained pipeline instance.

        Raises:
            PipelineNotFoundError: If this is called before .search() is called.
        """
        return self.__.best_pipeline

    import cloudpickle

    def save(
        self,
        file_path,
        pickle_type="cloudpickle",
        pickle_protocol=cloudpickle.DEFAULT_PROTOCOL,
    ):
        """Saves AutoML object at file path.

        Args:
            file_path (str): Location to save file.
            pickle_type ({"pickle", "cloudpickle"}): The pickling library to use.
            pickle_protocol (int): The pickle data stream format.

        Raises:
            ValueError: If pickle_type is not "pickle" or "cloudpickle".
        """
        return self.__.save(file_path, pickle_type, pickle_protocol)

    @staticmethod
    def load(
        file_path,
        pickle_type="cloudpickle",
    ):
        """Loads AutoML object at file path.

        Args:
            file_path (str): Location to find file to load
            pickle_type ({"pickle", "cloudpickle"}): The pickling library to use. Currently not used since the standard pickle library can handle cloudpickles.

        Returns:
            AutoSearchBase object
        """
        import pickle

        self = AutoMLSearch(empty=True)

        with open(file_path, "rb") as f:
            self.__ = pickle.load(f)

        return self

    def train_pipelines(self, pipelines):
        """Train a list of pipelines on the training data.

        This can be helpful for training pipelines once the search is complete.

        Args:
            pipelines (list[PipelineBase]): List of pipelines to train.

        Returns:
            Dict[str, PipelineBase]: Dictionary keyed by pipeline name that maps to the fitted pipeline.
            Note that the any pipelines that error out during training will not be included in the dictionary
            but the exception and stacktrace will be displayed in the log.
        """
        return self.__.train_pipelines(pipelines)

    def score_pipelines(self, pipelines, X_holdout, y_holdout, objectives):
        """Score a list of pipelines on the given holdout data.

        Args:
            pipelines (list[PipelineBase]): List of pipelines to train.
            X_holdout (pd.DataFrame): Holdout features.
            y_holdout (pd.Series): Holdout targets for scoring.
            objectives (list[str], list[ObjectiveBase]): Objectives used for scoring.

        Returns:
            dict[str, Dict[str, float]]: Dictionary keyed by pipeline name that maps to a dictionary of scores.
            Note that the any pipelines that error out during scoring will not be included in the dictionary
            but the exception and stacktrace will be displayed in the log.
        """
        return self.__.score_pipelines(pipelines, X_holdout, y_holdout, objectives)

    @property
    def plot(self):
        """Return an instance of the plot with the latest scores."""
        return self.__.plot

    def get_ensembler_input_pipelines(self, ensemble_pipeline_id):
        """Returns a list of input pipeline IDs given an ensembler pipeline ID.

        Args:
            ensemble_pipeline_id (id): Ensemble pipeline ID to get input pipeline IDs from.

        Returns:
            list[int]: A list of ensemble input pipeline IDs.

        Raises:
            ValueError: If `ensemble_pipeline_id` does not correspond to a valid ensemble pipeline ID.
        """
        return self.__.get_ensembler_input_pipelines(ensemble_pipeline_id)
