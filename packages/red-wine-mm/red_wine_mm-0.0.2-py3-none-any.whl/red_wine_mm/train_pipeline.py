from config.core import config
from pipeline import red_wine_pipe
from processing.data_manager import load_dataset, save_pipeline
from sklearn.model_selection import train_test_split


def run_training() -> None:
    """Train the model."""

    # read training data
    data = load_dataset(file_name=config.app_config.raw_data_file)

    # divide train and test
    X_train, X_test, y_train, y_test = train_test_split(
        data[config.m_config.features],  # predictors
        data[config.m_config.target],
        test_size=config.m_config.test_size,
        stratify=data[config.m_config.target],
        random_state=config.m_config.random_state,
    )

    # fit model
    red_wine_pipe.fit(X_train, y_train)

    # persist trained model
    save_pipeline(pipeline_to_persist=red_wine_pipe)


if __name__ == "__main__":
    run_training()
