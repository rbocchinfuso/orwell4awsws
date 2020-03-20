#!/usr/bin/env python
"""orwell4awsws.py: AWS Workspaces Access Monitor"""

import boto3, json, os, os.path, time, csv, configparser
from datetime import datetime
from pytz import timezone
from ISStreamer.Streamer import Streamer
from tqdm import tqdm
from daemonize import Daemonize

# owned
__author__ = 'Rich Bocchinfuso'
__copyright__ = 'Copyright 2020, Orwell for AWS Workspaces'
__credits__ = ['Rich Bocchinfuso']
__license__ = 'MIT'
__version__ = '0.2.0'
__maintainer__ = 'Rich Bocchinfuso'
__email__ = 'rbocchinfuso@gmail.com'
__status__ = 'Dev'

def createlogfile():
    # init csv log file
    utc_fileprefix = datetime.now(timezone('UTC'))
    est_fileprefix = utc_fileprefix.astimezone(timezone('US/Eastern'))
    logfileprefix = est_fileprefix.strftime(fileprefix_fmt)
    dailylogfile = config['local']['app_dir'] + config['local']['output_dir'] + logfileprefix + '_' + config['local']['log_file'] + '.csv'
    return (dailylogfile)

def uworkin(doh): 
    switcher = { 
        'CONNECTED':'ONLINE', 
        'DISCONNECTED':'OFFLINE', 
        'UNKNOWN':'OFFLINE', 
    }
    return switcher.get(doh, 'ERROR')

def spark(value):
    switcher = { 
        'OFFLINE':-100, 
        'ONLINE':100, 
    }
    return switcher.get(value, 'ERROR')

def runmode():
    if config['local']['run_mode'] == 'dev':
        print ('Running in dev mode. Using existing workspaces.json and connnections.json files.')
    elif config['local']['run_mode'] == 'test':
        print ('Running in test mode. Using existing workspaces.json and connnections.json files.')
    elif config['local']['run_mode'] == 'prod':
        os.system('aws workspaces describe-workspaces --max-items=1000 > workspaces.json') 
        os.system('aws workspaces describe-workspaces-connection-status --max-items=1000 > connections.json') 
    else:
        print ('Error: Invalid run mode')


def main():
    while True:
        utc_timestamp = datetime.now(timezone('UTC'))
        est = utc_timestamp.astimezone(timezone('US/Eastern'))
        est_timestamp = est.strftime(timestamp_fmt)
        est_date = est.strftime(date_fmt)
        est_time = est.strftime(time_fmt)

        runmode()

        log_file = createlogfile()

        if os.path.isfile(log_file):
            print ("File exist")
        else:
            with open(log_file, mode='w') as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                writer.writeheader()

        with open('connections.json') as connections_json_file:
            connections = json.load(connections_json_file)
        with open('workspaces.json') as workspaces_json_file:
            workspaces = json.load(workspaces_json_file)

        for w in workspaces['Workspaces']:
            print('collect_timestamp: ' + est_timestamp)
            workspace_id = (w['WorkspaceId'])
            print('workspace_id: ' + workspace_id)
            username = (w['UserName'])
            print('username: ' + username)
            workspace_runningmode = (w['WorkspaceProperties']['RunningMode'])
            print('workspace_runningmode: ' + workspace_runningmode)
            workspace_state = (w['State'])
            print('workspace_state: ' + workspace_state)
            for c in connections['WorkspacesConnectionStatus']:
                if c['WorkspaceId'] == workspace_id:
                    connection_state = (c['ConnectionState'])
                    print('connection_state: ' + connection_state)
                    user_state = uworkin(connection_state)
                    print('user_state: ' + user_state)
                    user_spark = spark(user_state)
                    # streamer.log(username, user_spark)
                    # streamer.log(username, user_state)
                    try:
                        epoch_conn_state_timestamp = (c['ConnectionStateCheckTimestamp'])
                        conn_state_timestamp = (time.strftime('%m-%d-%Y %H:%M:%S', time.localtime(epoch_conn_state_timestamp)))
                        print ('conn_state_timestamp: ' + conn_state_timestamp)
                    except:
                        print ('Exception Error')
                    try:
                        epoch_last_known_conn_timestamp = (c['LastKnownUserConnectionTimestamp'])
                        last_known_conn_timestamp = (time.strftime('%m-%d-%Y %H:%M:%S', time.localtime(epoch_last_known_conn_timestamp)))
                        print ('last_known_conn_timestamp: ' + last_known_conn_timestamp)
                    except:
                        print ('last_known_conn_timestamp: N/A')
            print('')
            with open(log_file,'a') as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                writer.writerow({'log_datestamp':est_date,'log_timestamp':est_time,'workspace_id':workspace_id, 'username':username, 'workspace_state':workspace_state, 'connection_state':connection_state, 'user_state':user_state, 'spark_metric':user_spark, 'connection_mins':(cycle_time/60), 'connection_hrs':(cycle_time/60/60), 'conn_state_timestamp':conn_state_timestamp, 'last_known_conn_timestamp':last_known_conn_timestamp})
            # flush data (force the buffer to empty and send)
            streamer.flush()

        # close the stream
        streamer.close()

        # cycle time
        # time.sleep(cycle_time)

        # visual cycle time
        for i in tqdm(range(cycle_time)):
            time.sleep(1)

if __name__ == "__main__":
    # time formats
    timestamp_fmt = '%Y-%m-%d %H:%M:%S %Z%z'
    date_fmt = '%m-%d-%Y'
    time_fmt = '%H:%M:%S'
    fileprefix_fmt = '%Y%m%d'

    # read and parse config file
    config = configparser.ConfigParser()
    config.read('config.ini')
    config.sections()

    cycle_time = int(config['local']['cycle_time'])
    fieldnames = ['log_datestamp', 'log_timestamp', 'workspace_id', 'username', 'workspace_state', 'connection_state', 'user_state', 'spark_metric', 'connection_mins', 'connection_hrs', 'conn_state_timestamp', 'last_known_conn_timestamp']

    # create or append to a streamer instance
    streamer = Streamer(bucket_name=config['initalstate']['bucket_name'], bucket_key=config['initalstate']['bucket_key'], access_key=config['initalstate']['access_key'])

    daemon = Daemonize(app="orwell4awsws", pid=config['local']['pid_file'], action=main, chdir=config['local']['app_dir'])
    daemon.start()