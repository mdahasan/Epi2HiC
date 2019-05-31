import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras.callbacks import ModelCheckpoint, EarlyStopping

import scipy.stats as st

meta_info = {
    'row': 8,
    'col': 100,
    'batch_size': 64,
    'epochs': 100
}


class Model(object):
    def __init__(self, data):
        super(Model, self).__init__()
        self.dataset = data.get_dataset_for_nn()

    def get_model_performance(self):
        return run_nn_model(self.dataset)


def run_nn_model(dataset):
    X_train = dataset['X_train']
    X_valid = dataset['X_valid']
    X_test = dataset['X_test']
    Y_train = dataset['Y_train']
    Y_valid = dataset['Y_valid']
    Y_test = dataset['Y_test']

    print X_train.shape
    print X_train[0].shape

    X_train = X_train.reshape(X_train.shape[0], meta_info['row'], meta_info['col'], 1)
    X_valid = X_valid.reshape(X_valid.shape[0], meta_info['row'], meta_info['col'], 1)
    X_test = X_test.reshape(X_test.shape[0], meta_info['row'], meta_info['col'], 1)
    input_shape = (meta_info['row'], meta_info['col'], 1)

    X_train = X_train.astype('float32')
    X_valid = X_valid.astype('float32')
    X_test = X_test.astype('float32')

    model = Sequential()
    model.add(Conv2D(64, kernel_size=(3, 3),
                     activation='relu',
                     input_shape=input_shape))
    model.add(Conv2D(64, (3,3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))
    model.add(Flatten())
    model.add(Dense(128, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(64, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(1, activation='linear'))

    model.compile(loss='mse',
                  optimizer=keras.optimizers.Adadelta())
    check_pointer = ModelCheckpoint(filepath='model.hdf5', verbose=1, monitor='val_loss', save_best_only=True)
    early_stopper = EarlyStopping(monitor='val_loss', patience=5, verbose=0)
    model.fit(X_train, Y_train,
              batch_size = meta_info['batch_size'],
              epochs = meta_info['epochs'],
              verbose = 1,
              shuffle = True,
              validation_data = (X_valid, Y_valid),
              callbacks = [check_pointer, early_stopper])

    Y_pred_train = model.predict(X_train)
    Y_pred_valid = model.predict(X_valid)
    Y_pred_test = model.predict(X_test)

    training_spearman = st.spearmanr(Y_train, Y_pred_train)
    valid_spearman = st.spearmanr(Y_valid, Y_pred_valid)
    test_spearman = st.spearmanr(Y_test, Y_pred_test)

    training_pearson = st.pearsonr(Y_train, Y_pred_train)
    valid_pearson = st.pearsonr(Y_valid, Y_pred_valid)
    test_pearson = st.pearsonr(Y_test, Y_pred_test)

    print training_spearman
    print training_spearman[0]

    print test_spearman
    print test_spearman[0]

    print training_pearson
    print training_pearson[0]

    print test_pearson
    print test_pearson[0]

    result = {
        'train_sp': training_spearman[0],
        'valid_sp': valid_spearman[0],
        'test_sp': test_spearman[0],
        'train_pr': training_pearson[0][0],
        'valid_pr': valid_pearson[0][0],
        'test_pr': test_pearson[0][0],
        'true_test_value': Y_test,
        'pred_test_value': Y_pred_test,
        'train_sample': len(Y_train),
        'valid_sample': len(Y_valid),
        'test_sample': len(Y_test)
    }

    return result
