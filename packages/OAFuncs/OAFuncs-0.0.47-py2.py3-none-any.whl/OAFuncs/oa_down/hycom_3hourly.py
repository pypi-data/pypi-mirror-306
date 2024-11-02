#!/usr/bin/env python
# coding=utf-8
'''
Author: Liu Kun && 16031215@qq.com
Date: 2024-11-01 10:31:09
LastEditors: Liu Kun && 16031215@qq.com
LastEditTime: 2024-11-02 12:14:33
FilePath: \\Python\\My_Funcs\\OAFuncs\\OAFuncs\\oa_down\\hycom_3hourly.py
Description:
EditPlatform: vscode
ComputerInfo: XPS 15 9510
SystemInfo: Windows 11
Python Version: 3.11
'''
import datetime
import os
import time
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests
from rich import print
from rich.progress import Progress

__all__ = ['draw_time_range', 'download', 'how_to_use']

# time resolution
data_info = {'yearly': {}, 'monthly': {}, 'daily': {}, 'hourly': {}}

# hourly data
# dataset: GLBv0.08, GLBu0.08, GLBy0.08
data_info['hourly']['dataset'] = {
    'GLBv0.08': {}, 'GLBu0.08': {}, 'GLBy0.08': {}}

# version
# version of GLBv0.08: 53.X, 56.3, 57.2, 92.8, 57.7, 92.9, 93.0
data_info['hourly']['dataset']['GLBv0.08']['version'] = {
    '53.X': {}, '56.3': {}, '57.2': {}, '92.8': {}, '57.7': {}, '92.9': {}, '93.0': {}}
# version of GLBu0.08: 93.0
data_info['hourly']['dataset']['GLBu0.08']['version'] = {'93.0': {}}
# version of GLBy0.08: 93.0
data_info['hourly']['dataset']['GLBy0.08']['version'] = {'93.0': {}}

# info details
# time range
# GLBv0.08
data_info['hourly']['dataset']['GLBv0.08']['version']['53.X']['time_range'] = {
    'time_start': '19940101', 'time_end': '20151230'}
data_info['hourly']['dataset']['GLBv0.08']['version']['56.3']['time_range'] = {
    'time_start': '20140701', 'time_end': '20160430'}
data_info['hourly']['dataset']['GLBv0.08']['version']['57.2']['time_range'] = {
    'time_start': '20160501', 'time_end': '20170131'}
data_info['hourly']['dataset']['GLBv0.08']['version']['92.8']['time_range'] = {
    'time_start': '20170201', 'time_end': '20170531'}
data_info['hourly']['dataset']['GLBv0.08']['version']['57.7']['time_range'] = {
    'time_start': '20170601', 'time_end': '20170930'}
data_info['hourly']['dataset']['GLBv0.08']['version']['92.9']['time_range'] = {
    'time_start': '20171001', 'time_end': '20171231'}
data_info['hourly']['dataset']['GLBv0.08']['version']['93.0']['time_range'] = {
    'time_start': '20180101', 'time_end': '20200218'}
# GLBu0.08
data_info['hourly']['dataset']['GLBu0.08']['version']['93.0']['time_range'] = {
    'time_start': '20180919', 'time_end': '20181208'}
# GLBy0.08
data_info['hourly']['dataset']['GLBy0.08']['version']['93.0']['time_range'] = {
    'time_start': '20181204', 'time_end': '20240904'}

# variable
variable_info = {
    'u': {'var_name': 'water_u', 'standard_name': 'eastward_sea_water_velocity'},
    'v': {'var_name': 'water_v', 'standard_name': 'northward_sea_water_velocity'},
    'temp': {'var_name': 'water_temp', 'standard_name': 'sea_water_potential_temperature'},
    'salinity': {'var_name': 'salinity', 'standard_name': 'sea_water_salinity'},
    'ssh': {'var_name': 'surf_el', 'standard_name': 'sea_surface_elevation'},
    'u_b': {'var_name': 'water_u_bottom', 'standard_name': 'eastward_sea_water_velocity_at_sea_floor'},
    'v_b': {'var_name': 'water_v_bottom', 'standard_name': 'northward_sea_water_velocity_at_sea_floor'},
    'temp_b': {'var_name': 'water_temp_bottom', 'standard_name': 'sea_water_potential_temperature_at_sea_floor'},
    'salinity_b': {'var_name': 'salinity_bottom', 'standard_name': 'sea_water_salinity_at_sea_floor'},
}

# classification method
# year_different: the data of different years is stored in different files
# same_path: the data of different years is stored in the same file
# var_different: the data of different variables is stored in different files
# var_year_different: the data of different variables and years is stored in different files
data_info['hourly']['dataset']['GLBv0.08']['version']['53.X']['classification'] = 'year_different'
data_info['hourly']['dataset']['GLBv0.08']['version']['56.3']['classification'] = 'same_path'
data_info['hourly']['dataset']['GLBv0.08']['version']['57.2']['classification'] = 'same_path'
data_info['hourly']['dataset']['GLBv0.08']['version']['92.8']['classification'] = 'var_different'
data_info['hourly']['dataset']['GLBv0.08']['version']['57.7']['classification'] = 'same_path'
data_info['hourly']['dataset']['GLBv0.08']['version']['92.9']['classification'] = 'var_different'
data_info['hourly']['dataset']['GLBv0.08']['version']['93.0']['classification'] = 'var_different'
data_info['hourly']['dataset']['GLBu0.08']['version']['93.0']['classification'] = 'var_different'
data_info['hourly']['dataset']['GLBy0.08']['version']['93.0']['classification'] = 'var_year_different'

# download info
# base url
# GLBv0.08 53.X
url_53x = {}
for y_53x in range(1994, 2016):
    # r'https://ncss.hycom.org/thredds/ncss/GLBv0.08/expt_53.X/data/2013?'
    url_53x[str(
        y_53x)] = rf'https://ncss.hycom.org/thredds/ncss/GLBv0.08/expt_53.X/data/{y_53x}?'
data_info['hourly']['dataset']['GLBv0.08']['version']['53.X']['url'] = url_53x
# GLBv0.08 56.3
data_info['hourly']['dataset']['GLBv0.08']['version']['56.3']['url'] = r'https://ncss.hycom.org/thredds/ncss/GLBv0.08/expt_56.3?'
# GLBv0.08 57.2
data_info['hourly']['dataset']['GLBv0.08']['version']['57.2']['url'] = r'https://ncss.hycom.org/thredds/ncss/GLBv0.08/expt_57.2?'
# GLBv0.08 92.8
url_928 = {
    'uv3z': r'https://ncss.hycom.org/thredds/ncss/GLBv0.08/expt_92.8/uv3z?',
    'ts3z': r'https://ncss.hycom.org/thredds/ncss/GLBv0.08/expt_92.8/ts3z?',
    'ssh': r'https://ncss.hycom.org/thredds/ncss/GLBv0.08/expt_92.8/ssh?',
}
data_info['hourly']['dataset']['GLBv0.08']['version']['92.8']['url'] = url_928
# GLBv0.08 57.7
data_info['hourly']['dataset']['GLBv0.08']['version']['57.7']['url'] = r'https://ncss.hycom.org/thredds/ncss/GLBv0.08/expt_57.7?'
# GLBv0.08 92.9
url_929 = {
    'uv3z': r'https://ncss.hycom.org/thredds/ncss/GLBv0.08/expt_92.9/uv3z?',
    'ts3z': r'https://ncss.hycom.org/thredds/ncss/GLBv0.08/expt_92.9/ts3z?',
    'ssh': r'https://ncss.hycom.org/thredds/ncss/GLBv0.08/expt_92.9/ssh?',
}
data_info['hourly']['dataset']['GLBv0.08']['version']['92.9']['url'] = url_929
# GLBv0.08 93.0
url_930_v = {
    'uv3z': r'https://ncss.hycom.org/thredds/ncss/GLBv0.08/expt_93.0/uv3z?',
    'ts3z': r'https://ncss.hycom.org/thredds/ncss/GLBv0.08/expt_93.0/ts3z?',
    'ssh': r'https://ncss.hycom.org/thredds/ncss/GLBv0.08/expt_93.0/ssh?',
}
data_info['hourly']['dataset']['GLBv0.08']['version']['93.0']['url'] = url_930_v
# GLBu0.08 93.0
url_930_u = {
    'uv3z': r'https://ncss.hycom.org/thredds/ncss/GLBu0.08/expt_93.0/uv3z?',
    'ts3z': r'https://ncss.hycom.org/thredds/ncss/GLBu0.08/expt_93.0/ts3z?',
    'ssh': r'https://ncss.hycom.org/thredds/ncss/GLBu0.08/expt_93.0/ssh?',
}
data_info['hourly']['dataset']['GLBu0.08']['version']['93.0']['url'] = url_930_u
# GLBy0.08 93.0
uv3z_930_y = {}
ts3z_930_y = {}
ssh_930_y = {}
for y_930_y in range(2018, 2025):
    uv3z_930_y[str(
        y_930_y)] = rf'https://ncss.hycom.org/thredds/ncss/GLBy0.08/expt_93.0/uv3z/{y_930_y}?'
    ts3z_930_y[str(
        y_930_y)] = rf'https://ncss.hycom.org/thredds/ncss/GLBy0.08/expt_93.0/ts3z/{y_930_y}?'
    ssh_930_y[str(
        y_930_y)] = rf'https://ncss.hycom.org/thredds/ncss/GLBy0.08/expt_93.0/ssh/{y_930_y}?'
url_930_y = {
    'uv3z': uv3z_930_y,
    'ts3z': ts3z_930_y,
    'ssh': ssh_930_y,
}
data_info['hourly']['dataset']['GLBy0.08']['version']['93.0']['url'] = url_930_y


def draw_time_range(pic_save_folder=None):
    if pic_save_folder is not None:
        os.makedirs(pic_save_folder, exist_ok=True)
    # Converting the data into a format suitable for plotting
    data = []
    for dataset, versions in data_info['hourly']['dataset'].items():
        for version, time_range in versions['version'].items():
            data.append({
                'dataset': dataset,
                'version': version,
                'start_date': pd.to_datetime(time_range['time_range']['time_start']),
                'end_date': pd.to_datetime(time_range['time_range']['time_end'])
            })

    # Creating a DataFrame
    df = pd.DataFrame(data)

    # Plotting with combined labels for datasets and versions on the y-axis
    plt.figure(figsize=(12, 6))

    # Combined labels for datasets and versions
    combined_labels = [f"{dataset}_{version}" for dataset,
                       version in zip(df['dataset'], df['version'])]

    colors = plt.cm.viridis(np.linspace(0, 1, len(combined_labels)))

    # Assigning a color to each combined label
    label_colors = {label: colors[i]
                    for i, label in enumerate(combined_labels)}

    # Plotting each time range
    k = 1
    for _, row in df.iterrows():
        plt.plot([row['start_date'], row['end_date']], [k, k],
                 color=label_colors[f"{row['dataset']}_{row['version']}"], linewidth=6)
        plt.text(row['end_date'], k,
                 f"{row['version']}", ha='right', color='black')
        k += 1

    # Setting the y-axis labels
    plt.yticks(range(1, len(combined_labels)+1), combined_labels)
    plt.xlabel('Time')
    plt.ylabel('Dataset - Version')
    plt.title('Time Range of Different Versions of Datasets')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    if pic_save_folder:
        plt.savefig(Path(pic_save_folder) / 'HYCOM_time_range.png')
    else:
        plt.savefig('HYCOM_time_range.png')
    # plt.show()
    plt.close()


def transform_time(time_str):
    # old_time = '2023080203'
    # time_new = '2023-08-02T03%3A00%3A00Z'
    time_new = f'{time_str[:4]}-{time_str[4:6]}-{time_str[6:8]}T{time_str[8:10]}%3A00%3A00Z'
    return time_new


def add_delta_time(dt, delta_hour):
    return dt + datetime.timedelta(hours=delta_hour)


def get_time_list(time_s, time_e, delta_hour):
    dt = datetime.datetime.strptime(time_s, '%Y%m%d%H')
    dt_list = []
    while dt.strftime('%Y%m%d%H') <= time_e:
        dt_list.append(dt.strftime('%Y%m%d%H'))
        dt = add_delta_time(dt, delta_hour)
    return dt_list


def get_nearest_level_index(depth):
    level_depth = [0.0, 2.0, 4.0, 6.0, 8.0, 10.0, 12.0, 15.0, 20.0, 25.0, 30.0, 35.0, 40.0, 45.0, 50.0, 60.0, 70.0, 80.0, 90.0, 100.0, 125.0,
                   150.0, 200.0, 250.0, 300.0, 350.0, 400.0, 500.0, 600.0, 700.0, 800.0, 900.0, 1000.0, 1250.0, 1500.0, 2000.0, 2500.0, 3000.0, 4000.0, 5000]
    return min(range(len(level_depth)), key=lambda i: abs(level_depth[i]-depth))


def set_query_dict(var, lon_min, lon_max, lat_min, lat_max, time_str_ymdh):
    query_dict = {
        'var': variable_info[var]['var_name'],
        'north': lat_max,
        'west': lon_min,
        'east': lon_max,
        'south': lat_min,
        'data_time': time_str_ymdh,
        'horizStride': 1,
        'addLatLon': 'true',
        'accept': 'netcdf4'
    }
    return query_dict


def get_query_dict_single_depth(var, lon_min, lon_max, lat_min, lat_max, depth, time_str_ymdh):
    query_dict = set_query_dict(
        var, lon_min, lon_max, lat_min, lat_max, time_str_ymdh)
    if var in ['u', 'v', 'temp', 'salinity']:
        print('Please ensure the depth is in the range of 0-5000 m')
        query_dict['vertCoord'] = get_nearest_level_index(depth)+1
    return query_dict


def get_query_dict_single_level(var, lon_min, lon_max, lat_min, lat_max, level_num, time_str_ymdh):
    # level_num: 1-40
    query_dict = set_query_dict(
        var, lon_min, lon_max, lat_min, lat_max, time_str_ymdh)
    if var in ['u', 'v', 'temp', 'salinity']:
        print('Please ensure the level_num is in the range of 1-40')
        if level_num == 0:
            level_num = 1
            print('The level_num is set to 1')
        if level_num > 40:
            level_num = 40
            print('The level_num is set to 40')
        query_dict['vertCoord'] = level_num
    return query_dict


def get_query_dict_full_level(var, lon_min, lon_max, lat_min, lat_max, time_str_ymdh):
    query_dict = set_query_dict(
        var, lon_min, lon_max, lat_min, lat_max, time_str_ymdh)
    if var in ['u', 'v', 'temp', 'salinity']:
        query_dict['vertStride'] = 1
    return query_dict


def get_query_dict_full_depth(var, lon_min, lon_max, lat_min, lat_max, time_str_ymdh):
    query_dict = set_query_dict(
        var, lon_min, lon_max, lat_min, lat_max, time_str_ymdh)
    if var in ['u', 'v', 'temp', 'salinity']:
        query_dict['vertStride'] = 1
    return query_dict


def ymd_in_which_dataset_and_version(time_ymd):
    time_ymd = int(time_ymd)
    d_list = []
    v_list = []
    trange_list = []
    for dataset_name in data_info['hourly']['dataset'].keys():
        for version_name in data_info['hourly']['dataset'][dataset_name]['version'].keys():
            # print(data_info['hourly']['dataset'][dataset_name]
            #       ['version'][version_name]['time_range'].values())
            time_s, time_e = list(
                data_info['hourly']['dataset'][dataset_name]['version'][version_name]['time_range'].values())
            if time_ymd >= int(time_s) and time_ymd <= int(time_e):
                d_list.append(dataset_name)
                v_list.append(version_name)
                trange_list.append(f'{time_s}-{time_e}')
    print(f'[bold red]{time_ymd} is in the following dataset and version:')
    for d, v, trange in zip(d_list, v_list, trange_list):
        # print(f'{time_ymd} is in {d} {v} {trange}')
        print(f'[bold blue]{d} {v} {trange}')


def direct_choose_dataset_and_version(time_ymd):
    time_ymd = int(time_ymd)
    for dataset_name in data_info['hourly']['dataset'].keys():
        for version_name in data_info['hourly']['dataset'][dataset_name]['version'].keys():
            [time_s, time_e] = list(data_info['hourly']['dataset'][dataset_name]['version'][version_name]['time_range'].values(
            ))
            # print(time_s, time_e, time_ymd)
            if time_ymd >= int(time_s) and time_ymd <= int(time_e):
                print(
                    f'[bold purple]dataset: {dataset_name}, version: {version_name} is chosen')
                # print(f'{time_ymd} is in {dataset_name} {version_name}')
                return dataset_name, version_name


def get_base_url(dataset_name, version_name, var, year_str):
    url_dict = data_info['hourly']['dataset'][dataset_name]['version'][version_name]['url']
    classification_method = data_info['hourly']['dataset'][dataset_name]['version'][version_name]['classification']
    if classification_method == 'year_different':
        base_url = url_dict[str(year_str)]
    elif classification_method == 'same_path':
        base_url = url_dict
    elif classification_method == 'var_different':
        if var in ['u', 'v', 'u_b', 'v_b']:
            base_url = url_dict['uv3z']
        elif var in ['temp', 'salinity', 'temp_b', 'salinity_b']:
            base_url = url_dict['ts3z']
        elif var in ['ssh']:
            base_url = url_dict['ssh']
        else:
            print(
                'Please ensure the var is in [u,v,temp,salinity,ssh,u_b,v_b,temp_b,salinity_b]')
    elif classification_method == 'var_year_different':
        if var in ['u', 'v', 'u_b', 'v_b']:
            base_url = url_dict['uv3z'][str(year_str)]
        elif var in ['temp', 'salinity', 'temp_b', 'salinity_b']:
            base_url = url_dict['ts3z'][str(year_str)]
        elif var in ['ssh']:
            base_url = url_dict['ssh'][str(year_str)]
        else:
            print(
                'Please ensure the var is in [u,v,temp,salinity,ssh,u_b,v_b,temp_b,salinity_b]')
    return base_url


def get_submit_url(dataset_name, version_name, var, year_str, query_dict):
    base_url = get_base_url(dataset_name, version_name, var, year_str)
    query_dict['var'] = [query_dict['var']]
    target_url = base_url + '&'.join(f"var={var}" for var in query_dict['var']) + '&' + '&'.join(
        f"{key}={value}" for key, value in query_dict.items() if key != 'var')
    return target_url


def clear_existing_file(file_full_path):
    if os.path.exists(file_full_path):
        os.remove(file_full_path)
        print(f'{file_full_path} has been removed')


def dlownload_file(target_url, store_path, file_name):
    # 创建会话
    s = requests.Session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'}

    download_success = False
    request_times = 0
    filename = Path(store_path) / file_name
    clear_existing_file(filename)
    while not download_success:
        if request_times > 0:
            print(f'\r正在重试第 {request_times} 次', end="")
        # 尝试下载文件
        try:
            response = s.get(target_url, headers=headers, stream=True)
            response.raise_for_status()  # 如果请求返回的不是200，将抛出HTTPError异常

            # 获取文件名
            """ content_disposition = response.headers.get('Content-Disposition')
            filename = content_disposition.split(
                "filename=")[1] if content_disposition else "hycom_data.nc" """

            # 保存文件
            with open(filename, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            # print(f'\r文件 {filename} 下载成功', end="")
            print(f'[bold green]文件 {filename} 下载成功')
            download_success = True

        except requests.exceptions.HTTPError as errh:
            print(f"Http Error: {errh}")
        except requests.exceptions.ConnectionError as errc:
            print(f"Error Connecting: {errc}")
        except requests.exceptions.Timeout as errt:
            print(f"Timeout Error: {errt}")
        except requests.exceptions.RequestException as err:
            print(f"OOps: Something Else: {err}")

        time.sleep(3)
        request_times += 1


def check_hour_is_valid(ymdh_str):
    # hour should be 00, 03, 06, 09, 12, 15, 18, 21
    hh = int(str(ymdh_str[-2:]))
    if hh in [0, 3, 6, 9, 12, 15, 18, 21]:
        return True
    else:
        return False


def direct_download(var, lon_min=0, lon_max=359.92, lat_min=-80, lat_max=90, download_time='2024083100', depth=None, level_num=None, store_path=None, dataset_name=None, version_name=None):
    time_ymd_str = str(download_time)[:8]
    if not check_hour_is_valid(download_time):
        print('Please ensure the hour is 00, 03, 06, 09, 12, 15, 18, 21')
        raise ValueError('The hour is invalid')
    if dataset_name is None and version_name is None:
        print('The dataset_name and version_name are None, so the dataset and version will be chosen according to the download_time.\nIf there is more than one dataset and version in the time range, the first one will be chosen.')
        print('If you wanna choose the dataset and version by yourself, please set the dataset_name and version_name together.')
        ymd_in_which_dataset_and_version(time_ymd_str)
        dataset_name, version_name = direct_choose_dataset_and_version(
            time_ymd_str)
    elif dataset_name is None and version_name is not None:
        print('Please ensure the dataset_name is not None')
        print('If you do not add the dataset_name, both the dataset and version will be chosen according to the download_time.')
        ymd_in_which_dataset_and_version(time_ymd_str)
        dataset_name, version_name = direct_choose_dataset_and_version(
            time_ymd_str)
    elif dataset_name is not None and version_name is None:
        print('Please ensure the version_name is not None')
        print('If you do not add the version_name, both the dataset and version will be chosen according to the download_time.')
        ymd_in_which_dataset_and_version(time_ymd_str)
        dataset_name, version_name = direct_choose_dataset_and_version(
            time_ymd_str)
    else:
        print('The dataset_name and version_name are both set by yourself.')

    year_str = str(download_time)[:4]
    if depth is not None and level_num is not None:
        print('Please ensure the depth or level_num is None')
    elif depth is not None:
        print(f'Data of single depth ({depth}m) will be downloaded...')
        query_dict = get_query_dict_single_depth(
            var, lon_min, lon_max, lat_min, lat_max, depth, download_time)
    elif level_num is not None:
        print(f'Data of single level ({level_num}) will be downloaded...')
        query_dict = get_query_dict_single_level(
            var, lon_min, lon_max, lat_min, lat_max, level_num, download_time)
    else:
        print('Full depth or full level data will be downloaded...')
        query_dict = get_query_dict_full_level(
            var, lon_min, lon_max, lat_min, lat_max, download_time)
    submit_url = get_submit_url(
        dataset_name, version_name, var, year_str, query_dict)
    file_name = f"HYCOM_{variable_info[var]['var_name']}_{download_time}.nc"
    if store_path is None:
        store_path = str(Path.cwd())
    else:
        os.makedirs(str(store_path), exist_ok=True)
    dlownload_file(submit_url, store_path, file_name)


def convert_full_name_to_short_name(full_name):
    for var, info in variable_info.items():
        if full_name == info['var_name'] or full_name == info['standard_name'] or full_name == var:
            return var
    print('[bold #FFE4E1]Please ensure the var is in:\n[bold blue]u,v,temp,salinity,ssh,u_b,v_b,temp_b,salinity_b')
    print('or')
    print('[bold blue]water_u, water_v, water_temp, salinity, surf_el, water_u_bottom, water_v_bottom, water_temp_bottom, salinity_bottom')
    return False


def download(var, ymdh_time_s, ymdh_time_e, lon_min=0, lon_max=359.92, lat_min=-80, lat_max=90,  depth=None, level_num=None, store_path=None, dataset_name=None, version_name=None):
    '''
    Description:
    Download the data of single time or a series of time

    Parameters:
    var: str, the variable name, such as 'u', 'v', 'temp', 'salinity', 'ssh', 'u_b', 'v_b', 'temp_b', 'salinity_b' or 'water_u', 'water_v', 'water_temp', 'salinity', 'surf_el', 'water_u_bottom', 'water_v_bottom', 'water_temp_bottom', 'salinity_bottom'
    ymdh_time_s: str, the start time, such as '2024110112'
    ymdh_time_e: str, the end time, such as '2024110212'
    lon_min: float, the minimum longitude, default is 0
    lon_max: float, the maximum longitude, default is 359.92
    lat_min: float, the minimum latitude, default is -80
    lat_max: float, the maximum latitude, default is 90
    depth: float, the depth, default is None
    level_num: int, the level number, default is None
    store_path: str, the path to store the data, default is None
    dataset_name: str, the dataset name, default is None
    version_name: str, the version name, default is None

    Returns:
    None
    '''
    var = convert_full_name_to_short_name(var)
    if var is False:
        raise ValueError('The var is invalid')
    if lon_min < 0 or lon_min > 359.92 or lon_max < 0 or lon_max > 359.92 or lat_min < -80 or lat_min > 90 or lat_max < -80 or lat_max > 90:
        print('Please ensure the lon_min, lon_max, lat_min, lat_max are in the range')
        print('The range of lon_min, lon_max is 0~359.92')
        print('The range of lat_min, lat_max is -80~90')
        raise ValueError('The lon or lat is invalid')
    ymdh_time_s = str(ymdh_time_s)
    ymdh_time_e = str(ymdh_time_e)
    if ymdh_time_s == ymdh_time_e:
        direct_download(var, lon_min, lon_max, lat_min, lat_max,
                        ymdh_time_s, depth, level_num, store_path, dataset_name, version_name)
    elif int(ymdh_time_s) < int(ymdh_time_e):
        print('Downloading a series of files...')
        time_list = get_time_list(ymdh_time_s, ymdh_time_e, 3)
        with Progress() as progress:
            task = progress.add_task(
                "[cyan]Downloading...", total=len(time_list))
            for time_str in time_list:
                direct_download(var, lon_min, lon_max, lat_min, lat_max,
                                time_str, depth, level_num, store_path, dataset_name, version_name)
                progress.update(task, advance=1)
    else:
        print('Please ensure the ymdh_time_s is less than the ymdh_time_e')


def how_to_use():
    print('''
    # 1. Choose the dataset and version according to the time:
    # 1.1 Use function to query
    You can use the function ymd_in_which_dataset_and_version(time_ymd=20241101) to find the dataset and version  according to the time.
    Then, you can see the dataset and version in the output.
    # 1.2 Draw a picture to see
    You can draw a picture to see the time range of each dataset and version.
    Using the function draw_time_range(pic_save_folder=None) to draw the picture.

    # 2. Get the base url according to the dataset, version, var and year:
    # 2.1 Dataset and version were found in step 1
    # 2.2 Var: u, v, temp, salinity, ssh, u_b, v_b, temp_b, salinity_b
    # 2.3 Year: 1994-2024(current year)

    # 3. Get the query_dict according to the var, lon_min, lon_max, lat_min, lat_max, depth, level_num, time_str_ymdh:
    # 3.1 Var: u, v, temp, salinity, ssh, u_b, v_b, temp_b, salinity_b
    # 3.2 Lon_min, lon_max, lat_min, lat_max: float
    # 3.3 Depth: 0-5000m, if you wanna get single depth data, you can set the depth
    # 3.4 Level_num: 1-40, if you wanna get single level data, you can set the level_num
    # 3.5 Time_str_ymdh: '2024110112', the hour normally is 00, 03, 06, 09, 12, 15, 18, 21, besides 1 hourly data
    # 3.6 Use the function to get the query_dict
    # 3.7 Note: If you wanna get the full depth or full level data, you can needn't set the depth or level_num

    # 4. Get the submit url according to the dataset, version, var, year, query_dict:
    # 4.1 Use the function to get the submit url
    # 4.2 You can use the submit url to download the data

    # 5. Download the data according to the submit url:
    # 5.1 Use the function to download the data
    # 5.2 You can download the data of single time or a series of time
    # 5.3 Note: If you wanna download a series of data, you can set the ymdh_time_s and ymdh_time_e different
    # 5.4 Note: The time resolution is 3 hours

    # 6. Direct download the data:
    # 6.1 Use the function to direct download the data
    # 6.2 You can set the dataset_name and version_name by yourself
    # 6.3 Note: If you do not set the dataset_name and version_name, the dataset and version will be chosen according to the download_time
    # 6.4 Note: If you set the dataset_name and version_name, please ensure the dataset_name and version_name are correct
    # 6.5 Note: If you just set one of the dataset_name and version_name, both the dataset and version will be chosen according to the download_time

    # 7. Simple use:
    # 7.1 You can use the function: download(var, ymdh_time_s, ymdh_time_e, lon_min=0, lon_max=359.92, lat_min=-80, lat_max=90,  depth=None, level_num=None, store_path=None, dataset_name=None, version_name=None)
    # 7.2 You can download the data of single time or a series of time
    # 7.3 The parameters you must set are var, ymdh_time_s, ymdh_time_e
    # 7.4 Example: download('u', '2024110112', '2024110212', lon_min=0, lon_max=359.92, lat_min=-80, lat_max=90,  depth=None, level_num=None, store_path=None, dataset_name=None, version_name=None)
    ''')


if __name__ == '__main__':
    download('v', '2024010200', '2024010300', lon_min=100, lon_max=150, lat_min=0,
             lat_max=50,  depth=0, store_path=r'I:\hycom_data_2024')
