
import pandas as pd
import numpy as np
ibsen_spinner = pd.read_csv("ibsenspinner.csv", sep=';',error_bad_lines=False)
push_kick = pd.read_csv("pushtokick.csv", sep=';',error_bad_lines=False)
normal_shots = pd.read_csv("mortenkick2.csv", sep=';',error_bad_lines=False)
alpha = 0.1
acc_sensitivity = 2048 / 90
gyro_sensitivity = 16.4
# https://bayesianadventures.wordpress.com/2013/10/20/gyroscopes-accelerometers-and-the-complementary-filter/
# lets use scaling factors according to MPU6050 documentation

def smoothing(df, alpa):
    array_x = [df['x'][0] * alpha]
    array_y = [df['y'][0] * alpha]
    array_z = [df['z'][0] * alpha]
    array_rx = [df['rx'][0] * alpha]
    array_ry = [df['ry'][0] * alpha]
    array_rz = [df['rz'][0] * alpha]
    
    for i in range(1,df.shape[0]):
        array_x.append(array_x[i-1]+alpha*(df['x'][i] - array_x[i-1]))
        array_y.append(array_y[i-1]+alpha*(df['y'][i] - array_y[i-1]))
        array_z.append(array_z[i-1]+alpha*(df['z'][i] - array_z[i-1]))
        array_rx.append(array_rx[i-1]+alpha*(df['rx'][i] - array_rx[i-1]))
        array_ry.append(array_ry[i-1]+alpha*(df['rz'][i] - array_ry[i-1]))
        array_rz.append(array_rz[i-1]+alpha*(df['ry'][i] - array_rz[i-1]))
        
    df['x'] = array_x
    df['y'] = array_y
    df['z'] = array_z
    df['rx'] = array_rx
    df['ry'] = array_ry
    df['rz'] = array_rz
    return df

ibsen_spinner = smoothing(ibsen_spinner,alpha)
push_kick = smoothing(push_kick,alpha)
normal_shots = smoothing(normal_shots,alpha)

def make_acc_angle(df,acc_sensitivity):
    df['x_ang'] = df['x'] / acc_sensitivity
    df['y_ang'] = df['y'] / acc_sensitivity
    df['z_ang'] = df['z'] / acc_sensitivity
    df['x_ang'] = df['x_ang']
    return df
    
def make_gyro_rate(df, gyro_sensitivity):
    df['rx_rate'] = df['rx'] / gyro_sensitivity
    df['ry_rate'] = df['ry'] / gyro_sensitivity
    df['rz_rate'] = df['rz'] / gyro_sensitivity
    return df

# get the sample rate:
def get_sample_frequency(sample_times):
    for i in range(1, len(sample_times)):
        if sample_times[i] >= 1000:
            return i
        
ibsen_spinner = make_acc_angle(ibsen_spinner,acc_sensitivity)
ibsen_spinner = make_gyro_rate(ibsen_spinner,gyro_sensitivity)

push_kick = make_acc_angle(push_kick, acc_sensitivity)
push_kick = make_gyro_rate(push_kick,gyro_sensitivity)

normal_shots = make_acc_angle(normal_shots, acc_sensitivity)
normal_shots = make_gyro_rate(normal_shots,gyro_sensitivity)

sf = get_sample_frequency(ibsen_spinner['time'])


ibsen_spinner['roll'] = np.zeros(len(ibsen_spinner['x']))

push_kick['roll'] = np.zeros(len(push_kick['y']))

normal_shots['roll'] = np.zeros(len(normal_shots['y']))

dt = float(1.0 / sf)

# initilize first acc on 

#using complementary filter formel from: https://bayesianadventures.wordpress.com/2013/10/20/gyroscopes-accelerometers-and-the-complementary-filter/
# this is bit expensive, dunno how to transform this for vectorisation

def complementary_filter(df):
    alpha = 0.2
    roll = [(1 - alpha) * (df['rx_rate'][0]*dt) + alpha * df['x_ang'][0]]
    for index in range(1,df.shape[0]):
        roll.append((1-alpha)*(roll[index-1]) + (df['rx_rate'][index]*dt) + alpha * df['x_ang'][index])
    return (roll)


(roll) = complementary_filter(ibsen_spinner)
ibsen_spinner['roll'] = roll

(roll) = complementary_filter(push_kick)
push_kick['roll'] = roll

(roll) = complementary_filter(normal_shots)
normal_shots['roll'] = roll


# this methods calculates the total rotation and acc
def calc_toal_acc(df, sens):
    df['total_acc'] = np.sqrt((df['x']**2) + (df['y']**2) +(df['z']**2))
    # dividing by the acc_sensitivity
    df['total_acc'] = df['total_acc'] / 2048
    return df

ibsen_spinner = calc_toal_acc(ibsen_spinner, acc_sensitivity)
push_kick = calc_toal_acc(push_kick,acc_sensitivity)
normal_shots = calc_toal_acc(normal_shots,acc_sensitivity)


#filter
#currently not used
def remove_noise(df):
    result = abs(df['total_acc'].pct_change())
    result = result.apply(lambda x: x > 0.5)
    df = df[result]
    print df.shape
    df = df.reset_index(drop=True)
    return df

def is_noise(row):
    # rest value around 1g
    if (abs(row['roll'] < 20)) and ((row['total_acc'] < 1.3) and not (row['total_acc'] < 0.8)):
        return True
    return False

def extract_movement(df,index):
    j = 1
    length = df.shape[0]
    movement = [df.iloc[index]]
    while True:
        if j + index >= length:
            return (movement, j)
        if not is_noise(df.iloc[index+j]):
            movement.append(df.iloc[index + j])
            j = j + 1
        else:
            n = 100
            result = find_next_move(df, index + j, length,n)
            if result > n:
                return (movement, j)
            else:
                for x in range(1,result+1):
                    movement.append(df.iloc[index + j + x])
                j = j + result
                
def find_next_move(df, start_index, max_length, n):
    offset = 1
    while offset < n:
        if (offset + start_index) > max_length-1:
            return offset
        elif not is_noise(df.iloc[start_index + offset]):
            return offset
        offset = offset + 1
    return offset + 1
            

def get_movements(df):
    movements = []
    data_length = df.shape[0]
    print data_length
    iterable = iter(xrange(data_length))    
    for i in iterable:
        if not is_noise(df.iloc[i]):
            (movement, index) = extract_movement(df,i+1)
            [iterable.next() for x in range(index)]
            if len(movement) > 0:
                movements.append(movement)
    return movements        

ibsen_spinners = get_movements(ibsen_spinner)
pushes = get_movements(push_kick)
normals = get_movements(normal_shots)

def cut_shorts(df):
    result = []
    for i in range(len(df)):
        if len(df[i]) > 20:
            result.append(df[i])
    return result

ibsen_spinners = cut_shorts(ibsen_spinners)
pushes = cut_shorts(pushes)
normals = cut_shorts(normals)

from sklearn.cluster import KMeans

# idea: use USL to cluster for x,y,z
# total clusters is: n * 3
def group_shots(shots, n):
    trains = []
    for shot in shots:
        x = []
        y = []
        z = []
        for point in shot:
            x.append(point['x'])
            y.append(point['y'])
            z.append(point['z'])
        x = np.array(x)
        y = np.array(y)
        z = np.array(z)
        kmeans_x = KMeans(n_clusters=n, random_state=0).fit(x.reshape(-1,1))
        kmeans_y = KMeans(n_clusters=n, random_state=0).fit(y.reshape(-1,1))
        kmeans_z = KMeans(n_clusters=n, random_state=0).fit(z.reshape(-1,1))
        trains.append(np.array([kmeans_x,kmeans_y,kmeans_z]))
    print "printing len of trains"
    print len(trains)
    return trains
# make these into dataframes or something similar
ibsen_grouped = group_shots(ibsen_spinners,5)
pushes_grouped = group_shots(pushes,5)
normals_grouped = group_shots(normals,5)


# now make 15 input neurons for each shots

def get_center_cords(shots):
    input_neurons_shots = []
    print "len"
    print len(shots)
    for group in shots:
        input_neurons_shot = []
        for clusters in group:
            cluster_centers = clusters.cluster_centers_
            for center in cluster_centers:
                input_neurons_shot.append(center[0])
        input_neurons_shots.append(input_neurons_shot)
        #input_neurons_shot = group.cluster_centers_
    return np.array(input_neurons_shots)
type_ibsen = np.array(get_center_cords(ibsen_grouped))
type_push = np.array(get_center_cords(pushes_grouped))
type_normals = np.array(get_center_cords(normals_grouped))


# make test, trains and labels
test_ibsen = type_ibsen[-2:]
type_ibsen = type_ibsen[:-2]


test_push = type_push[-2:]
type_push = type_push[:-2]

test_normals = type_normals[-2:]
type_normals = type_normals[:-2]


labels_ibsen = np.zeros(len(type_ibsen))
labels_push = np.zeros(len(type_push))
labels_push = labels_push + 1
labels_normals = np.zeros(len(type_normals))
labels_normals = labels_normals + 2

# lets make an ANN
from sklearn.neural_network import MLPClassifier
clf = MLPClassifier(solver='lbfgs', alpha=1e-5, random_state=1)


merged_train = np.concatenate([type_ibsen, type_push, type_normals])
merged_labels = np.concatenate([labels_ibsen, labels_push, labels_normals])


clf.fit(merged_train,merged_labels)

# should all be 0
print clf.predict(type_ibsen)

# should all be 1
clf.predict(type_push)

#should all be 2
clf.predict(type_normals)


pred_ibsen = clf.predict(test_ibsen)
accuracy = len(pred_ibsen[pred_ibsen == 0]) / float(len(pred_ibsen))
print accuracy

