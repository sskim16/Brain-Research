import argparse
import math
import numpy as np

import os, sys
import time
from datetime import datetime
from threading import Timer

from pythonosc import dispatcher
from pythonosc import osc_server

server = None
eeg = alpha = beta = delta = gamma = theta = thetaBetaRatio = 0
eeg_values = []
alpha_values = []
beta_values = []
gamma_values = []
delta_values = []
theta_values = []
count = 1

finished_phase = 0
calibrate_time = 30
test_time = calibrate_time

calibration_values = {}
calibration_means = {}
calibration_stds = {}
chw_calibration_mean = {}

def eeg_handler(unused_addr, args, ch1, ch2, ch3, ch4):
    global eeg, count
    #print("EEG (uV) per channel: ", ch1, ch2, ch3, ch4)
    eeg_values.append([ch1, ch2, ch3, ch4])
    #eeg = (eeg + ch1 + ch2 + ch3 + ch4)
    #eeg = egg/4


def eeg_handler1(unused_addr, args, ch1, ch2, ch3, ch4):
    #print("Absolute ALPHA Wave: ", ch1, ch2, ch3, ch4)
    alpha_values.append([ch1, ch2, ch3, ch4])
    #alpha = (alpha + ch1 + ch2 + ch3 + ch4)
    #alpha = alpha/4	

def eeg_handler2(unused_addr, args, ch1, ch2, ch3, ch4):
    #print("Absolute BETA Wave: ", ch1, ch2, ch3, ch4)
    beta_values.append([ch1, ch2, ch3, ch4])
    #beta = (beta+ ch1 + ch2 + ch3 + ch4)
    #beta = beta/4	

def eeg_handler3(unused_addr, args, ch1, ch2, ch3, ch4):
    #print("Absolute DELTA Wave: ", ch1, ch2, ch3, ch4)
    delta_values.append([ch1, ch2, ch3, ch4])
    #delta = (delta + ch1 + ch2 + ch3 + ch4)
    #delta = delta/4	

def eeg_handler4(unused_addr, args, ch1, ch2, ch3, ch4):
    #print("Absolute GAMMA Wave: ", ch1, ch2, ch3, ch4)
    gamma_values.append([ch1, ch2, ch3, ch4])
    #gamma = (gamma + ch1 + ch2 + ch3 + ch4)
    #gamma = gamma/4	

def eeg_handler5(unused_addr, args, ch1, ch2, ch3, ch4):
    #print("Absolute THETA Wave: ", ch1, ch2, ch3, ch4)
    theta_values.append([ch1, ch2, ch3, ch4])
    #theta = (theta + ch1 + ch2 + ch3 + ch4)
    #theta = theta/4	

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip",
                        default="127.0.0.1",
                        help="The ip to listen on")
    parser.add_argument("--port",
                        type=int,
                        default=5000,
                        help="The port to listen on")
    args = parser.parse_args()

def exitfunc():
    global finished_phase
    server.shutdown()
    global eeg_values, alpha_values, beta_values, gamma_values, delta_values, theta_values
    print ("Exit Time", datetime.now())
    eeg_values = np.array(eeg_values)
    alpha_values = np.array(alpha_values)
    beta_values = np.array(beta_values)
    gamma_values = np.array(gamma_values)
    delta_values = np.array(delta_values)
    theta_values = np.array(theta_values)

    calibration_values['eeg'] = eeg_values
    calibration_values['alpha'] = alpha_values
    calibration_values['beta'] = beta_values
    calibration_values['gamma'] = gamma_values
    calibration_values['delta'] = delta_values
    calibration_values['theta'] = theta_values

    eeg_means = np.mean(eeg_values, axis=0)
    alpha_means = np.mean(alpha_values, axis=0)
    beta_means = np.mean(beta_values, axis=0)
    gamma_means = np.mean(gamma_values, axis=0)
    delta_means = np.mean(delta_values, axis=0)
    theta_means = np.mean(theta_values, axis=0)

    eeg_stdev = np.std(eeg_values, axis=0)
    alpha_stdev = np.std(alpha_values, axis=0)
    beta_stdev = np.std(beta_values, axis=0)
    gamma_stdev = np.std(gamma_values, axis=0)
    delta_stdev = np.std(delta_values, axis=0)
    theta_stdev = np.std(theta_values, axis=0)

    calibration_means['eeg'] = eeg_means
    calibration_means['alpha'] = alpha_means
    calibration_means['beta'] = beta_means
    calibration_means['gamma'] = gamma_means
    calibration_means['delta'] = delta_means
    calibration_means['theta'] = theta_means

    calibration_stds['eeg'] = eeg_stdev
    calibration_stds['alpha'] = alpha_stdev
    calibration_stds['beta'] = beta_stdev
    calibration_stds['gamma'] = gamma_stdev
    calibration_stds['delta'] = delta_stdev
    calibration_stds['theta'] = theta_stdev

    print ("Absolute Alpha Wave Chnl Avg: ", alpha_means)
    print ("Alpha Wave Standard Devs:", alpha_stdev)
    print ("Absolute Beta Wave Chnl Avg: ", beta_means)
    print ("Alpha Wave Standard Devs:", beta_stdev)
    print ("Absolute Delta Wave Chnl Avg: ", delta_means)
    print ("Alpha Wave Standard Devs:", delta_stdev)
    print ("Absolute Gamma Wave Chnl Avg: ", gamma_means)
    print ("Alpha Wave Standard Devs:", gamma_stdev)
    print ("Absolute Theta Wave Chnl Avg: ", theta_means)
    print ("Alpha Wave Standard Devs:", theta_stdev)

    eeg_means = np.mean(eeg_values)
    alpha_means = np.mean(alpha_values)
    beta_means = np.mean(beta_values)
    gamma_means = np.mean(gamma_values)
    delta_means = np.mean(delta_values)
    theta_means = np.mean(theta_values)
    thetaBetaRatio = theta_means/beta_means

    chw_calibration_mean['eeg'] = eeg_means
    chw_calibration_mean['alpha'] = alpha_means
    chw_calibration_mean['beta'] = beta_means
    chw_calibration_mean['gamma'] = gamma_means
    chw_calibration_mean['delta'] = delta_means
    chw_calibration_mean['theta'] = theta_means

    print ("Absolute Alpha Wave Avg: ", alpha_means)
    print ("Absolute Beta Wave Avg: ", beta_means)
    print ("Absolute Delta Wave Avg: ", delta_means)
    print ("Absolute Gamma Wave Avg: ", gamma_means)
    print ("Absolute Theta Wave Avg: ", theta_means)
    print ("Theta/Beta Ratio: ", thetaBetaRatio)
    #os._exit(0)
    finished_phase = 1

Timer(calibrate_time, exitfunc).start() # exit in 30 seconds

dispatcher = dispatcher.Dispatcher()
dispatcher.map("/debug", print)
dispatcher.map("/muse/eeg", eeg_handler, "EEG")
dispatcher.map("/muse/elements/alpha_absolute", eeg_handler1, "ALPHA")
dispatcher.map("/muse/elements/beta_absolute", eeg_handler2, "BETA")
dispatcher.map("/muse/elements/delta_absolute", eeg_handler3, "DELTA")
dispatcher.map("/muse/elements/gamma_absolute", eeg_handler4, "GAMMA")
dispatcher.map("/muse/elements/theta_absolute", eeg_handler5, "THETA")
server = osc_server.ThreadingOSCUDPServer(
    (args.ip, args.port), dispatcher)
print("Serving on {}".format(server.server_address))
server.serve_forever()

while not(finished_phase):
    print (finished_phase)
    time.sleep(1)

print("waiting for input...")
input()

def second_exitfunc():
    server.shutdown()
    global eeg_values, alpha_values, beta_values, gamma_values, delta_values, theta_values
    print ("\n------TEST DATA------")
    print ("Exit Time", datetime.now())
    eeg_values = np.array(eeg_values)
    alpha_values = np.array(alpha_values)
    beta_values = np.array(beta_values)
    gamma_values = np.array(gamma_values)
    delta_values = np.array(delta_values)
    theta_values = np.array(theta_values)

    test_eeg_means = np.mean(eeg_values, axis=0)
    test_alpha_means = np.mean(alpha_values, axis=0)
    test_beta_means = np.mean(beta_values, axis=0)
    test_gamma_means = np.mean(gamma_values, axis=0)
    test_delta_means = np.mean(delta_values, axis=0)
    test_theta_means = np.mean(theta_values, axis=0)

    test_eeg_stdev = np.std(eeg_values, axis=0)
    test_alpha_stdev = np.std(alpha_values, axis=0)
    test_beta_stdev = np.std(beta_values, axis=0)
    test_gamma_stdev = np.std(gamma_values, axis=0)
    test_delta_stdev = np.std(delta_values, axis=0)
    test_theta_stdev = np.std(theta_values, axis=0)

    print ("Absolute Alpha Wave Chnl Avg: ", test_alpha_means)
    print ("Alpha Wave Standard Devs:", test_alpha_stdev)
    print ("Absolute Beta Wave Chnl Avg: ", test_beta_means)
    print ("Alpha Wave Standard Devs:", test_beta_stdev)
    print ("Absolute Delta Wave Chnl Avg: ", test_delta_means)
    print ("Alpha Wave Standard Devs:", test_delta_stdev)
    print ("Absolute Gamma Wave Chnl Avg: ", test_gamma_means)
    print ("Alpha Wave Standard Devs:", test_gamma_stdev)
    print ("Absolute Theta Wave Chnl Avg: ", test_theta_means)
    print ("Alpha Wave Standard Devs:", test_theta_stdev)

    test_eeg_means = np.mean(eeg_values)
    test_alpha_means = np.mean(alpha_values)
    test_beta_means = np.mean(beta_values)
    test_gamma_means = np.mean(gamma_values)
    test_delta_means = np.mean(delta_values)
    test_theta_means = np.mean(theta_values)
    test_thetaBetaRatio = test_theta_means/test_beta_means

    print ("Absolute Alpha Wave Avg: ", test_alpha_means)
    print ("Absolute Beta Wave Avg: ", test_beta_means)
    print ("Absolute Delta Wave Avg: ", test_delta_means)
    print ("Absolute Gamma Wave Avg: ", test_gamma_means)
    print ("Absolute Theta Wave Avg: ", test_theta_means)
    print ("Theta/Beta Ratio: ", test_thetaBetaRatio)

    if test_thetaBetaRatio > 3:
        print ("There is a high probability that you may have ADHD. You may want to get evaluated by a professional.")     

    #eab = np.mean(theta_values.reshape(-1).dot(beta_values.reshape(-1)))
    #cov = eab - test_theta_means * test_beta_means
    #print ("Covariance could possibly be ", cov)
    cov = np.cov(theta_values.reshape(-1), beta_values.reshape(-1))[0][1]
    print ("Covariance is", cov)
    #print ("Effect size", abs((test_theta_means - test_beta_means) / cov))
    '''
    TODO: compare with calibration values
    '''
    if test_thetaBetaRatio > 3:
        print ("There is a high probability that you may have ADHD. You may want to get evaluated by a professional.")
    else:
        print ("Thank you for using this ADHD screening!")

    sys.exit(0)

eeg_values = []
alpha_values = []
beta_values = []
gamma_values = []
delta_values = []
theta_values = []

Timer(test_time, second_exitfunc).start() # exit in 30 seconds

server.serve_forever()