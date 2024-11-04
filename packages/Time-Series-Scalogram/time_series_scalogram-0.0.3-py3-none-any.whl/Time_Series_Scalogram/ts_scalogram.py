import numpy as np
from multiprocessing import Pool
from scipy.optimize import curve_fit
from scipy import stats
from scipy.spatial.distance import jensenshannon
import pickle
import tqdm
import pandas as pd
from gc import collect
import sys
import time
from pathlib import Path
import pandas as pd
from pathlib import Path
# from pixel_func import func


def calc_xinds(index, t_step, use_pandas=True):

    print("t step: %s" % t_step)

    tgrid0 = pd.Timestamp(index[0]).ceil('1min')
    nxgrid = (index[-1] - tgrid0)/t_step
    xgrid = np.arange(tgrid0, index[-1], t_step)
    print("length of xgrid: %d, tstep=%s, range: %s -> %s" %(len(xgrid), pd.Timedelta(t_step), pd.Timestamp(xgrid[0]), pd.Timestamp(xgrid[-1])))

    xinds = np.zeros(len(xgrid), dtype = int)
    xind_last = int(0)
    jumpsize = int(5*len(index)/((index[-1]-index[0])/np.timedelta64(1,'s'))*t_step/np.timedelta64(1,'s'))
    for i1, xg in enumerate(xgrid):
        xg = xgrid[i1]
        try:
            xind_diff = int(np.where(index[xind_last:xind_last+jumpsize] <= xg)[0][-1])
        except:
            xind_diff = int(np.where(index[xind_last:] <= xg)[0][-1])
        xind_new = xind_diff+xind_last
        xinds[i1] = xind_new
        xind_last = xind_new

    xinds_infos = {
        'xinds': xinds,
        'xgrid': xgrid,
        'nxgrid': nxgrid,
        'jumpsize': jumpsize,
        't_step': t_step
    }

    return xinds_infos


import importlib.util
import sys
from pathlib import Path

def load_user_defined_function(pixel_func_path=None):
    # Load the function from the specified path or fall back to the local pixel_func module
    if pixel_func_path is None:
        func = pixel_funcs.compressbility
    else:
        # Create a unique name for the module to avoid conflicts
        module_name = "user_pixel_func"
        pixel_func_path = Path(pixel_func_path).absolute()
        
        # Load the module from the specified path
        spec = importlib.util.spec_from_file_location(module_name, pixel_func_path)
        user_pixel_func = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = user_pixel_func
        spec.loader.exec_module(user_pixel_func)
        
        # Fetch the function
        func = user_pixel_func.func

        # Print the location of the loaded module
        print(f"Loaded function from: {user_pixel_func.__file__}")
    

    return func



def TimeSeriesScalogram(
    series,
    wins,
    t_step,
    verbose = True,
    Ncores = 8,
    step_win_ratio = 0.01,
    savpath = './',
    savname = "results_%03d.pkl",
    chunksize = 1000,
    pixel_func_path = None,
): 

    """
    Time Series Scalogram
    This function generate a 2D matrix with the pixel value determined by func. The y-axis is window size, and the x-axis is time.
    Input:
        series: pandas Series
        func: function to calculate the pixel value
        settings: dictionary
            wins: numpy array of np.timedelta64
            step: np.timedelta64
            
    """

    func = load_user_defined_function(pixel_func_path)

    # Calculate xgrid
    xinds_infos = calc_xinds(series.index, t_step, use_pandas=False)
    xinds = xinds_infos['xinds']
    xgrid = xinds_infos['xgrid']

    steps = np.zeros_like(wins)
    step_ratio_set = 1/step_win_ratio
    step_ratio_0 = int(wins[0]/t_step)

    tstart_list = []
    tend_list = []
    print("--------------------------------------------\nStep Win Ratio: %s\n--------------------------------------------\n" % step_win_ratio)
    for i1, win in enumerate(wins):
        step_ratio = (win/t_step)
        if step_ratio < step_ratio_set:
            step_factor = 1
        else:
            step_factor = np.floor(step_ratio/step_ratio_set)

        steps[i1] = t_step * step_factor

        if i1 % 10 == 0:
            print(win, steps[i1], 1/step_ratio, step_factor, int((xgrid[-1]-xgrid[0])/steps[i1]))

        # calculate tstart_list and tend_list
        tstart_list_temp = np.arange(xgrid[0], xgrid[-1], np.timedelta64(steps[i1],'ns'))
        tend_list_temp = tstart_list_temp + win
        if i1 == 0 :
            tstart_list = tstart_list_temp
            tend_list = tend_list_temp
        else:
            tstart_list = np.append(tstart_list, tstart_list_temp)
            tend_list = np.append(tend_list, tend_list_temp)

    # randomize tstart_list and tend_list with the same indices
    inds = np.arange(len(tstart_list))
    np.random.shuffle(inds)
    tstart_list = tstart_list[inds]
    tend_list = tend_list[inds]


    N = len(xgrid) * len(wins)
    N1 = len(tstart_list)

    alloc_input = {
        'series': series,
        'func': func,
        'xinds': xinds,
        'xgrid': xgrid,
        'tstart_list': tstart_list,
        'tend_list': tend_list,
    }



    # print information

    if verbose:
        print("\n")
        print("-------------------------------------------")
        print("           Time Series Scalogram           ")
        print("-------------------------------------------")
        print("\n")
        print("---- Settings ----\n")
        
        print("win: %s -> %s, N = %d" % (wins[0], wins[-1], len(wins)))
        print("step: %s" % t_step)
        print("Ncores: %s" % Ncores)
        print("chunksize: %s" % chunksize)


        print('xgrid: %s - %s, len: %s' %(pd.Timestamp(xgrid[0]), pd.Timestamp(xgrid[-1]), pd.Timedelta(xgrid[-1]-xgrid[0])))
        print("\nTotal Pixels= %d\n" %(N))
        print("\nTotal Iterations= %d\n" %(N1))
    

        total_size = 0
        for key, value in alloc_input.items():
            size_in_bytes = sys.getsizeof(value)
            size_in_mb = size_in_bytes / (1024 * 1024)
            total_size += size_in_mb
            print("Size of %s: %.4f MB" %(key, size_in_mb))

        print(">>> Total size: %.4f MB <<<\n" %(total_size))


        print("Number of cores: %d" % Ncores)
        print("Savpath: ", savpath)
        print("Savname: ", savname)
        print("\n>>>>>>> Start Scanner Parallel >>>>>>>\n")

    settings = {
        'wins': wins,
        'step': t_step,
        'Ncores': Ncores,
        'savpath': savpath,
        'savname': savname,
        'chunksize': chunksize,
        'verbose': verbose,
        'xgrid': xgrid,
        'step_win_ratio': step_win_ratio,
        'xinds': xinds
    }

    
    # check the existing dataframe files:
    final_name = Path(savpath).joinpath('df_'+savname % (0))
    if Path(final_name).is_file():
        print("File already exists: %s\n" % final_name)
        # continue
    
    # ===== main loop ===== #
    scanstemp = []
    with Pool(Ncores, initializer=InitParallelAllocation, initargs=(alloc_input,)) as p:
        for scan in tqdm.tqdm(p.imap_unordered(SolarWindScannerInnerLoopParallel, range(0, N1), chunksize), total=N1):
            scanstemp.append(scan)


    # turn scans into dataframe
    dfpath = Path(savpath).joinpath('df_'+savname % (0))
    scansdf = pd.DataFrame(scanstemp)
    pd.to_pickle(scansdf, dfpath)
    print("Saved at: %s\n" % dfpath)

    # save the settings
    with open(Path(savpath).joinpath('settings.pkl'), 'wb') as f:
        pickle.dump(settings, f)

    scans = scanstemp

    return scans, settings


def InitParallelAllocation(alloc_input):
    global series, func, xinds, xgrid, tstart_list, tend_list

    series = alloc_input['series']
    func = alloc_input['func']
    xinds = alloc_input['xinds']
    xgrid = alloc_input['xgrid']
    tstart_list = alloc_input['tstart_list']
    tend_list = alloc_input['tend_list']



def SolarWindScannerInnerLoopParallel(i1):
    # access global variables
    global series, func, xinds, xgrid, tstart_list, tend_list

    values0 = series.values


    tstart= tstart_list[i1]
    tend = tend_list[i1]
    win = tend - tstart

    try:
        id0 = xinds[int(np.where(xgrid == tstart)[0][0])]
        id1 = xinds[int(np.where(xgrid == tend)[0][0])]


        values = values0[id0:id1]

        nan_infos = {
            'ids': {'id0': id0, 'id1': id1, 'len': len(values)}
        }
        nan_infos['flag'] = 1
    except:
        values = None
        nan_infos = {
            'ids': {'id0': np.nan, 'id1': np.nan, 'skip_size': np.nan, 'len': np.nan}
        }
        nan_infos['flag'] = 0


    scan = func(values)

    scan['nan_infos'] = nan_infos
    scan['t0'] = tstart
    scan['t1'] = tend
    scan['win'] = win
    scan['tmid'] = tstart + win/2

    return scan


class pixel_funcs:
    def compressbility(x):
        try:

            scan = {
                'value': np.sum(np.abs(np.log10(x)) > 0.02)/len(x),
            }

        except:
            scan = {
                'value': np.nan
            }

        return scan



def calc_js_distance(x0, nbins = 101, n_sigma = 5):
    """
    calculate js distance
    x0: numpy array
    """
    try:
        x = x0

        # rescale x
        x = (x-np.mean(x))/np.std(x)

        # calculate pdf of x
        bins = np.linspace(-n_sigma, n_sigma, nbins)
        hist_data, bin_edges_data = np.histogram(x, bins=bins, density=True)
        outside_count = np.sum(x < bins[0]) + np.sum(x > bins[-1])


        # Compute the PDF of the Gaussian distribution at the mid-points of the histogram bins
        bin_midpoints = bin_edges_data[:-1] + np.diff(bin_edges_data) / 2
        pdf_gaussian = stats.norm.pdf(bin_midpoints, 0, 1)

        js_div = jensenshannon(hist_data, pdf_gaussian)

        scan = {
            'js': js_div,
            'outside_count': outside_count,
            'mean': np.mean(x0),
            'std': np.std(x0),
            'skew': stats.skew(x0),
            'kurt': stats.kurtosis(x0)
        }

    except:
        scan = {
            'js': np.nan,
            'outside_count': np.nan,
            'mean': np.nan,
            'std': np.nan,
            'skew': np.nan,
            'kurt': np.nan
        }

    return scan