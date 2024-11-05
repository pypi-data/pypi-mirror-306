from synapse.plugins.categories.base import Action
from synapse.utils.file import get_dict_from_file, files_url_to_path_from_objs
from synapse.utils.module_loading import import_string


class TrainAction(Action):
    # TODO implement specifying which hardware to use (gpu-n, cpu)

    def get_input_dataset_for_training(self, model_id=None):
        """
        :return:
        {
            "train": [
                {
                    "files": {
                        "image": {
                            "path": "/path/to/image.jpg",
                            "meta": {
                                "width": 265,
                                "height": 190,
                                "created": 1651563526.0277045,
                                "file_size": 5191,
                                "last_modified": 1651563526.0277045
                            }
                        }
                    },
                    "ground_truth": {
                        ...label_data
                    }
                },
                ...
            ],
            "validation": ...,
            "test": ...
        }
        """

        client = self.logger.client
        input_dataset = {}
        category_int_to_str = {1: 'train', 2: 'validation', 3: 'test'}

        if client:
            train_dataset, count_dataset = client.list_train_dataset(
                payload={'fields': ['category', 'files', 'ground_truth'], 'model': model_id}, list_all=True
            )

            for i, train_data in enumerate(train_dataset, start=1):
                self.set_progress(i, count_dataset, category='dataset_download')
                category = category_int_to_str[train_data.pop('category')]
                try:
                    input_dataset[category].append(train_data)
                except KeyError:
                    input_dataset[category] = [train_data]

        else:
            for category in category_int_to_str.values():
                dataset_path = self.task['dataset'].get(category)
                if dataset_path:
                    input_dataset[category] = get_dict_from_file(dataset_path)
                    files_url_to_path_from_objs(input_dataset[category], ['files'], is_list=True)

        return input_dataset

    def run_train(self):
        hyperparameter = self.task['hyperparameter']
        train = import_string(self.plugin['train']['entrypoint'])

        # download dataset
        self.log_event('Preparing dataset for training.')
        input_dataset = self.get_input_dataset_for_training()

        # train dataset
        self.log_event('Starting model training.')

        model_files = train(self, input_dataset, hyperparameter)

        # upload model_data
        self.log_event('Registering model data.')

        self.end_log()
        return model_files

    def start(self):
        action = self.task['action']
        getattr(self, f'run_{action}')()

    def log_metric(self, x, i, **kwargs):
        self.log(x, {x: i, **kwargs})

    def log_model(self, files, status=None):
        pass
