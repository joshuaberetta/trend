import pandas as pd
from yaml import safe_load
from .trend import misc_gis, pipeline


def main():
    
    ###### INPUT ########
    
    CONFIG_PATH = 'config.yaml'
        
    #####################
    
    with open(CONFIG_PATH, 'r') as opened_file:
        config = safe_load(opened_file)
    
    settings = config['settings']
    date_range = settings['date_range']
    data = config['data']
    misc = data['gis']['misc']
    variables = data['variables']
    
    gis = misc_gis(misc['geo_db_path'], misc['dams_of_interest'], misc['layers'])
    nodes = pd.read_csv(data['nodes'])
    
    for d_type, values in variables.items():
        pipeline(path=values['path'], gis=gis, nodes=nodes, d_type=d_type, 
                 unit=values['unit'], plot_title=values['title'], 
                 start_year=date_range['start_year'], end_year=date_range['end_year'], 
                 cmap=settings['cmap'], shape_path=data['gis']['shape_path'], 
                 groups=settings['groups'], folder=settings['out_folder'], 
                 save=True, save_gif=True)


if __name__ == '__main__':
    main()