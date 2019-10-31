import os, sys
from glob import glob

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta
from yaml import safe_load
from typing import List, Dict, Union

from openpyxl import load_workbook
import fiona
from shapely.geometry import shape, mapping
import cartopy.crs as ccrs
import imageio

import matplotlib
import matplotlib.pyplot as plt

from .databunch import DataBunch
from .progress import printProgressBar


months = {1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 
          6: "June", 7: "July", 8: "August", 9: "September", 10: "October", 
          11: "November", 12: "December"}


def get_month(month, group):
    return group[month]


def combine(path, nodes, group=['yearly', 'monthly'], d_type=None, save=False):
        
    combined = []
    for _, nodes in nodes.iterrows():
        node, quat = nodes

        file_name = f'{node}.dat'
        
        try:
            data = DataBunch(path, file_name, quat, d_type)
        
            if group == 'yearly':
                summary = data.yearly_mean()
            elif group == 'monthly':
                summary = data.monthly_mean()

            combined.append(summary)
        
        except:
            continue
    
    group_type = group.capitalize()[:-2]
    combined = (pd.concat(combined)
                .sort_values(by=['Quat', group_type])
                .reset_index(drop=True))
    
    if save:
        combined.to_csv(f'{d_type}_{group_type}.csv', index=False)
    else:
        return combined


def summarise(df, nodes, group=['yearly', 'monthly'], d_type=None):
    
    quats = set(nodes['Quat'])
    grp = group[:-2].capitalize()
    
    li = []
    for quat in quats:
        filt = df[df['Quat'] == quat]
        grouped = filt.groupby([grp]).mean()
        df_out = pd.DataFrame(data={
            'Quat':quat,
            f'{grp}':grouped.index,
            f'{d_type}':grouped[d_type]
        })

        df_out.index.name = None
        df_out = df_out.reset_index(drop=True)

        li.append(df_out)
    
    return pd.concat(li).sort_values(['Quat', grp]).reset_index(drop=True)


def mkdirs(group, d_type, folder):
    
    Path(f'{folder}/').mkdir(parents=True, exist_ok=True)
    
    f = f'{d_type}_{group}'
    img_path = Path(f'{folder}/plots/')
    gif_path = Path(f'{folder}/gifs/')
    
    img_dest = img_path/f
    img_dest.mkdir(parents=True, exist_ok=True)
    
    gif_dest = gif_path
    gif_dest.mkdir(parents=True, exist_ok=True)


def gif(img_path, group, folder):
    durations = {'yearly': 0.5, 'monthly': 1}
    images = []
    for file in glob(f'{folder}/plots/{img_path}/*.png'):
        images.append(imageio.imread(file))
    imageio.mimsave(f'{folder}/gifs/{img_path}.gif', images, duration=durations[group])


def plot_map(df, gis, group=['yearly', 'monthly'], d_type=None, unit='', 
             plot_title='', start_year=1920, end_year=2010, cmap='viridis', 
             shape_path='', save=False, save_loc=None) -> None:

    max_val = df[d_type].max()
    crs = ccrs.Mercator()
    group_type = group.capitalize()[:-2]
    
    if group == 'yearly':
        rng = range(start_year, end_year+1)
    elif group == 'monthly':
        rng = range(1, 13)

    len_rng = len(rng)
    printProgressBar(0, len_rng, prefix=f'Progress ({d_type}, {group}):', suffix='Complete', length=50)
    
    for i, item in enumerate(rng):

        printProgressBar(i + 1, len_rng, prefix=f'Progress ({d_type}, {group}):', suffix='Complete', length=50)

        cmap = matplotlib.cm.get_cmap(cmap)
        norm = matplotlib.colors.Normalize(0, max_val)
        color_producer = matplotlib.cm.ScalarMappable(norm=norm, cmap=cmap)
        fig, ax = plt.subplots(figsize=(20, 20), subplot_kw={'projection': crs})     
        
        with fiona.open(shape_path) as src:
            for feature in src:
                properties = feature['properties']
                quat = properties['CATNUM']
                
                if quat in df['Quat'].to_list():
                    try:
                        index = df[(df['Quat'] == quat)&(df[group_type] == item)][d_type].iloc[0]
                    except:
                        continue
                elif quat.startswith('C2'): 
                    index = None
                else:
                    index = -9.9
                
                geom = shape(feature['geometry'])
                
                if index is None:
                    continue
                elif index >= 0:
                    rgba = color_producer.to_rgba(index)
                    ax.add_geometries([geom], crs, facecolor=rgba, edgecolor='grey', linewidth=0.5)
                else:
                    ax.add_geometries([geom], crs, facecolor='white', edgecolor='grey', linewidth=0.5)
                
                
                pnt = geom.centroid
                x, y = pnt.x, pnt.y
                
                ax.annotate(quat, ax.projection.transform_point(x, y, crs),
                           horizontalalignment='center', verticalalignment='bottom', size=10, color='darkgrey')

        dams = gis['dams']
        for i in range(len(dams)):
            geom = shape(dams[i]['geometry'])
            ax.add_geometries([geom], crs, color='skyblue', edgecolor='royalblue')

        with fiona.open(shape_path) as src:
            for feature in src:
                properties = feature['properties']
                quat = properties['CATNUM']
                
                if quat in df['Quat'].to_list():
                    try:
                        index = df[(df['Quat'] == quat)&(df[group_type] == item)][d_type].iloc[0]
                    except:
                        continue
                elif quat.startswith('C2'): 
                    index = None
                else:
                    index = -9.9
                
                geom = shape(feature['geometry'])
                
                if index is None:
                    continue
                elif index >= 0:
                    rgba = color_producer.to_rgba(index)
                    ax.add_geometries([geom], crs, facecolor='none', edgecolor='grey', linewidth=0.5)
                else:
                    ax.add_geometries([geom], crs, facecolor='none', edgecolor='grey', linewidth=0.5)
        
        mask = gis['mask']
        for i in range(len(mask)):
            geom = shape(mask[i]['geometry'])
            ax.add_geometries([geom], crs, facecolor='none', edgecolor='black', linewidth=2)

        cats = gis['catchments']
        for i in range(len(cats)):
            cat = cats[i]['properties']['MOD_Catch']
            geom = shape(cats[i]['geometry'])
            ax.add_geometries([geom], crs,edgecolor='black', facecolor='none', linewidth=0.7)
            pnt = geom.centroid
            x, y = pnt.x, pnt.y
            ax.annotate(cat, ax.projection.transform_point(x, y, crs),
                        horizontalalignment='center', verticalalignment='center', size=12,
                        fontweight='ultralight')
                        
        ax.set_xlim(27.5,30.5)
        ax.set_ylim(-29,-26.1)
        sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)  
        matplotlib.rcParams.update({'font.size': 15})
        fig.colorbar(sm, fraction=0.044, pad=0.04) 
        
        if group == 'yearly':
            out_file = f'{d_type}_{item}.png'
            title = f"{plot_title} ({unit})\n{item}\n"
        elif group == 'monthly':
            title = f"{plot_title} ({unit})\n{get_month(item, months)}\n"
            if item < 10:
                item = f'0{item}'
            out_file = f'{d_type}_{item}.png'
        
        plt.title(title, size=30)
        
        if save:               
            fig.savefig(f'{save_loc}/{out_file}')
            plt.close(fig)
        else: 
            plt.show()


def pipeline(path, gis, nodes, d_type, unit, plot_title, start_year, end_year, cmap, shape_path,
             groups=['yearly', 'monthly'], save=False, save_gif=False, folder='test') -> None:
    
    for group in groups:
        df = combine(path, nodes, group, d_type)
        df = summarise(df, nodes, group, d_type)
        mkdirs(group, d_type, folder)
        plot_map(df, gis, group, d_type=d_type, unit=unit, plot_title=plot_title,
                 start_year=start_year, end_year=end_year, cmap=cmap, shape_path=shape_path,
                save=save, save_loc=f'{folder}/plots/{d_type}_{group}')
        if save_gif:
            gif(img_path=f'{d_type}_{group}', group=group, folder=folder)


def misc_gis(geo_db_path:str, dams_of_interest:list, layers:Dict[str,str]) -> Dict[str, list]:

    misc = {}
    for _ in fiona.listlayers(geo_db_path):
        for layer, layer_name in layers.items():               
            features = get_feats(geo_db_path, layer_name, dams_of_interest)
            misc[layer] = features
                
    return misc


def get_feats(geo_db_path:str, layer_name:str, dams_of_interest:list) -> list:
    
    features = []
    with fiona.open(geo_db_path, layer=layer_name) as src:
        if layer_name == 'Dams':
            for feature in src:
                if feature['properties']['Dam_Name'] in dams_of_interest:
                    features.append(feature)
        else:
            for feature in src:
                features.append(feature)
    
    return features