import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def log_performance(MSE, MAE, Pearson_r, R2, Spearman_r, sqrt_MSE):
    # create a file handler
    handler = logging.FileHandler('./log/logs.log')
    handler.setLevel(logging.INFO)
    # create a logging format
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    # add the handlers to the logger
    logger.addHandler(handler)
    logger.info('MSE: %s, MAE: %s, Pearson_r: %s, R2: %s, Spearman_r: %s, sqrt_MSE: %s', MSE, MAE, Pearson_r, R2,
                Spearman_r, sqrt_MSE)
    logger.removeHandler(handler)  # remove the Handler after you finish your job


def log_state(msg):
    # create a file handler
    handler = logging.FileHandler('./log/logs.log')
    handler.setLevel(logging.INFO)
    # create a logging format
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    # add the handlers to the logger
    logger.addHandler(handler)
    logger.info(msg)
    logger.removeHandler(handler)
