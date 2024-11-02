import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import datetime
import numpy as np
import pandas as pd
import seaborn as sns
import xarray as xr
from matplotlib.dates import DateFormatter
from pandas import DataFrame
from scipy import stats
from skyfield import almanac
from skyfield import api
from tqdm import tqdm
import matplotlib.colors as mcolors
import gsw
import cartopy.crs as ccrs
import cartopy.feature as cfeature


def _necessary_variables_check(ds: xr.Dataset, vars: list):
    """Checks that all of a list of variables are present in a dataset

    Args:
        ds (xarray.Dataset): _description_
        vars (list): _description_

    Raises:
        KeyError: Raises an error if all vars not present in ds
    """
    missing_vars = set(vars).difference(set(ds.variables))
    if missing_vars:
        msg = f"Required variables {list(missing_vars)} do not exist in the suppllied dataset."
        raise KeyError(msg)
    

def grid2d(x, y, v, xi=1, yi=1):
    """
    Function to grid data
    
    Parameters
    ----------
    x: data with data for the x dimension
    y: data with data for the y dimension
    v: data with data for the z dimension
    xi: Horizontal resolution for the gridding
    yi: Vertical resolution for the gridding
                
    Returns
    -------
    grid: z data gridded in x and y space with xi and yi resolution
    XI: x data gridded in x and y space with xi and yi resolution
    YI: y data gridded in x and y space with xi and yi resolution

    """
    if np.size(xi) == 1:
        xi = np.arange(np.nanmin(x), np.nanmax(x) + xi, xi)
    if np.size(yi) == 1:
        yi = np.arange(np.nanmin(y), np.nanmax(y) + yi, yi)
    raw = pd.DataFrame({'x': x, 'y': y, 'v': v}).dropna()
    grid = np.full([np.size(xi), np.size(yi)], np.nan)
    raw['xbins'], xbin_iter = pd.cut(raw.x, xi, retbins=True, labels=False)
    raw['ybins'], ybin_iter = pd.cut(raw.y, yi, retbins=True, labels=False)
    _tmp = raw.groupby(['xbins', 'ybins'])['v'].agg('median')
    grid[_tmp.index.get_level_values(0).astype(int), _tmp.index.get_level_values(1).astype(int)] = _tmp.values
    YI, XI = np.meshgrid(yi, xi)
    return grid, XI, YI


def updown_bias(ds, var='PSAL', v_res=1):
    """
    This function computes up and downcast averages for a specific variable

    Parameters
    ----------
    ds: xarray on OG1 format containing at least time, depth, latitude, longitude and the selected variable. 
        Data should not be gridded.
    var: Selected variable
    v_res: Vertical resolution for the gridding
                
    Returns
    -------
    df: pandas dataframe containing dc (Dive - Climb average), cd (Climb - Dive average) and depth

    """
    _necessary_variables_check(ds, ['PROFILE_NUMBER', 'DEPTH', var])
    p = 1  # Horizontal resolution
    z = v_res  # Vertical resolution
    if var in ds.variables:
        varG, profG, depthG = grid2d(ds.PROFILE_NUMBER, ds.DEPTH, ds[var], p, z)

        grad = np.diff(varG, axis=0)  # Horizontal gradients

        dc = np.nanmean(grad[0::2, :], axis=0)  # Dive - CLimb
        cd = np.nanmean(grad[1::2, :], axis=0)  # Climb - Dive

        df = pd.DataFrame(data={'dc': dc, 'cd': cd, 'depth': depthG[0, :]})
    else:
        print(f'{var} is not in the dataset')
        df = pd.DataFrame()

    return df


def plot_updown_bias(df: pd.DataFrame, ax: plt.Axes = None, xlabel='Temperature [C]', **kw: dict, ) -> tuple({plt.Figure, plt.Axes}):
    """
    This function can be used to plot the up and downcast differences computed with the updown_bias function
    
    Parameters
    ----------
    df: pandas dataframe containing dc (Dive - Climb average), cd (Climb - Dive average) and depth
    ax: axis to plot the data
    xlabel: label for the x-axis
    
    Returns
    -------
    A line plot comparing the day and night average over depth for the selected day
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(5, 5))
    else:
        fig = plt.gcf()

    if not all(hasattr(df, attr) for attr in ['dc', 'depth']):
        ax.text(0.5, 0.55, xlabel, va='center', ha='center', transform=ax.transAxes, bbox=dict(facecolor='white', alpha=0.5, edgecolor='none'))
        ax.text(0.5, 0.45, 'data unavailable', va='center', ha='center', transform=ax.transAxes, bbox=dict(facecolor='white', alpha=0.5, edgecolor='none'))
    else:
        ax.plot(df.dc, df.depth, label='Dive-Climb')
        ax.plot(df.cd, df.depth, label='Climb-Dive')
        ax.legend(loc=3)
        lims = np.abs(df.dc)
        ax.set_xlim(-np.nanpercentile(lims, 99.5), np.nanpercentile(lims, 99.5))
        ax.set_ylim(df.depth.max() + 1, -df.depth.max() / 30)
    ax.set_xlabel(xlabel)
    ax.grid()
    return fig, ax


def find_cline(var, depth_array):
    """
    Find the depth of the maximum vertical difference for a specified variables
    Input data has to be gridded
    """
    clin = np.where(np.abs(np.diff(np.nanmean(var, axis=0))) == np.nanmax(np.abs(np.diff(np.nanmean(var, axis=0)))))
    return np.round(depth_array[0, clin[0]], 1)


def plot_basic_vars(ds, v_res=1, start_prof=0, end_prof=-1):
    """
    This function plots the basic oceanographic variables temperature, salinity and density. A second plot is created and filled with oxygen and 
    chlorophyll data if available.
    
    Parameters
    ----------
    ds: xarray in OG1 format containing at least temperature, salinity and density and depth
    v_res: vertical resolution for the gridding. Horizontal resolution (by profile) is assumed to be 1
    start_prof: start profile used to compute the means that will be plotted. This can vary in case the dataset spread over a large timescale
                or region and subsections want to be plotted-1     
    end_prof: end profile used to compute the means that will be plotted. This can vary in case the dataset spread over a large timescale
              or region and subsections want to be plotted-1          
    
    Returns
    -------
    Line plots for the averages of the different variables. 
    Thermo, halo and pycnocline are computed and plotted. A sentence stating the depth of the clines is printed too
    """
    _necessary_variables_check(ds, ['PROFILE_NUMBER', 'DEPTH', 'TEMP', 'PSAL'])
    p = 1
    z = v_res
    tempG, profG, depthG = grid2d(ds.PROFILE_NUMBER, ds.DEPTH, ds.TEMP, p, z)
    salG, profG, depthG = grid2d(ds.PROFILE_NUMBER, ds.DEPTH, ds.PSAL, p, z)

    if 'DENSITY' not in ds.variables:
        ds['DENSITY'] = (('N_MEASUREMENTS'), np.full(ds.dims['N_MEASUREMENTS'], np.nan))
        SA = gsw.SA_from_SP(ds.PSAL, ds.DEPTH, ds.LONGITUDE, ds.LATITUDE)
        CT = gsw.CT_from_t(SA, ds.TEMP, ds.DEPTH)
        ds['DENSITY'] = gsw.rho(SA, CT, ds.DEPTH)

    denG, profG, depthG = grid2d(ds.PROFILE_NUMBER, ds.DEPTH, ds.DENSITY, p, z)

    tempG = tempG[start_prof:end_prof, :]
    salG = salG[start_prof:end_prof, :]
    denG = denG[start_prof:end_prof, :]
    depthG = depthG[start_prof:end_prof, :]

    halo = find_cline(salG, depthG)
    thermo = find_cline(tempG, depthG)
    pycno = find_cline(denG, depthG)
    print(
        f'The thermocline, halocline and pycnocline are located at respectively {thermo}, {halo} and {pycno}m as shown in the plots as well')

    fig, ax = plt.subplots(1, 2, figsize=(15, 5))
    ax1 = ax[0].twiny()
    ax2 = ax[0].twiny()
    ax2.spines["top"].set_position(("axes", 1.2))
    ax[0].plot(np.nanmean(tempG, axis=0), depthG[0, :], c='blue')
    ax1.plot(np.nanmean(salG, axis=0), depthG[0, :], c='red')
    ax2.plot(np.nanmean(denG, axis=0), depthG[0, :], c='black')
    ax[0].axhline(thermo, linestyle='dashed', c='blue')
    ax1.axhline(halo, linestyle='dashed', c='red')
    ax2.axhline(pycno, linestyle='dashed', c='black')

    ax[0].set(xlabel=f'Average Temperature [C] \nbetween profile {start_prof} and {end_prof}', ylabel='Depth (m)')
    ax[0].tick_params(axis='x', colors='blue')
    ax[0].xaxis.label.set_color('blue')
    ax1.spines['bottom'].set_color('blue')
    ax1.set(xlabel=f'Average Salinity [PSU] \nbetween profile {start_prof} and {end_prof}')
    ax1.xaxis.label.set_color('red')
    ax1.spines['top'].set_color('red')
    ax1.tick_params(axis='x', colors='red')
    ax2.spines['bottom'].set_color('black')
    ax2.set(xlabel=f'Average Density [kg m-3] \nbetween profile {start_prof} and {end_prof}')
    ax2.xaxis.label.set_color('black')
    ax2.spines['top'].set_color('black')
    ax2.tick_params(axis='x', colors='black')

    if 'CHLA' in ds.variables:
        chlaG, profG, depthG = grid2d(ds.PROFILE_NUMBER, ds.DEPTH, ds.CHLA, p, z)
        chlaG = chlaG[start_prof:end_prof, :]
        ax2_1 = ax[1].twiny()
        ax2_1.plot(np.nanmean(chlaG, axis=0), depthG[0, :], c='green')
        ax2_1.set(xlabel=f'Average Chlorophyll-a [mg m-3] \nbetween profile {start_prof} and {end_prof}')
        ax2_1.xaxis.label.set_color('green')
        ax2_1.spines['top'].set_color('green')
        ax2_1.tick_params(axis='x', colors='green')
    else:
        ax[1].text(0.3, 0.7, 'Chlorophyll data unavailable', va='top', transform=ax[1].transAxes)

    if 'DOXY' in ds.variables:
        oxyG, profG, depthG = grid2d(ds.PROFILE_NUMBER, ds.DEPTH, ds.DOXY, p, z)
        oxyG = oxyG[start_prof:end_prof, :]
        ax[1].plot(np.nanmean(oxyG, axis=0), depthG[0, :], c='orange')
        ax[1].set(xlabel=f'Average Oxygen [mmol m-3] \nbetween profile {start_prof} and {end_prof}')
        ax[1].xaxis.label.set_color('orange')
        ax[1].spines['top'].set_color('orange')
        ax[1].tick_params(axis='x', colors='orange')
        ax[1].spines['bottom'].set_color('orange')
    else:
        ax[1].text(0.3, 0.5, 'Oxygen data unavailable', va='top', transform=ax[1].transAxes)

    [a.set_ylim(depthG.max() + 10, -5) for a in ax]
    [a.grid() for a in ax]
    return fig, ax


def optics_first_check(ds, var='CHLA'):
    """
    Function to assess any drift in deep optics data and the presence of any possible negative data
    This function returns plots and text
    """
    _necessary_variables_check(ds, [var, 'TIME', 'DEPTH'])
    # Check how much negative data there is
    neg_chl = np.round((len(np.where(ds[var] < 0)[0]) * 100) / len(ds[var]), 1)
    if neg_chl > 0:
        print(f'{neg_chl}% of scaled {var} data is negative, consider recalibrating data')
        # Check where the negative values occur and if we just see them at specific time of the mission or not
        start = ds.TIME[np.where(ds[var] < 0)][0]
        end = ds.TIME[np.where(ds[var] < 0)][-1]
        min_z = ds.DEPTH[np.where(ds[var] < 0)].min().values
        max_z = ds.DEPTH[np.where(ds[var] < 0)].max().values
        print(f'Negative data in present from {str(start.values)[:16]} to {str(end.values)[:16]}')
        print(f'Negative data is present between {"%.1f" % np.round(min_z, 1)} and {"%.1f" % np.round(max_z, 1)} ')
    else:
        print(f'There is no negative scaled {var} data, recalibration and further checks are still recommended ')
    # Check if there is any missing data throughout the mission
    if len(ds.TIME) != len(ds[var].dropna(dim='N_MEASUREMENTS').TIME):
        print(f'{var} data is missing for part of the mission')  # Add to specify where the gaps are
    else:
        print(f'{var} data is present for the entire mission duration')
    # Check bottom dark count and any drift there
    bottom_opt_data = ds[var].where(ds[var].DEPTH > ds.DEPTH.max() - (ds.DEPTH.max() * 0.1)).dropna(
        dim='N_MEASUREMENTS')
    slope, intercept, r_value, p_value, std_err = stats.linregress(np.arange(0, len(bottom_opt_data)), bottom_opt_data)
    ax = sns.regplot(data=ds, x=np.arange(0, len(bottom_opt_data)), y=bottom_opt_data,
                     scatter_kws={"color": "grey"},
                     line_kws={"color": "red", "label": "y={0:.8f}x+{1:.5f}".format(slope, intercept)},
                     )
    ax.legend(loc=2)
    ax.grid()
    ax.set(ylim=(np.nanpercentile(bottom_opt_data, 0.5), np.nanpercentile(bottom_opt_data, 99.5)),
           xlabel='Measurements',
           ylabel=var)
    percentage_change = (((slope * len(bottom_opt_data) + intercept) - intercept) / abs(intercept)) * 100

    if abs(percentage_change) >= 1:
        print(
            'Data from the deepest 10% of data has been analysed and data does not seem perfectly stable. An alternative solution for dark counts has to be considered. \nMoreover, it is recommended to check the sensor has this may suggest issues with the sensor (i.e water inside the sensor, temporal drift etc)')
        print(
            f'Data changed (increased or decreased) by {"%.1f" % np.round(percentage_change, 1)}% from the beginning to the end of the mission')
    else:
        print(
            f'Data from the deepest 10% of data has been analysed and data seems stable. These deep values can be used to re-assess the dark count if the no {var} at depth assumption is valid in this site and this depth')
    return ax


def sunset_sunrise(time, lat, lon):
    """
    Calculates the local sunrise/sunset of the glider location from GliderTools.
    [https://github.com/GliderToolsCommunity/GliderTools/blob/master/glidertools/optics.py]

    The function uses the Skyfield package to calculate the sunrise and sunset
    times using the date, latitude and longitude. The times are returned
    rather than day or night indices, as it is more flexible for the quenching
    correction.


    Parameters
    ----------
    time: numpy.ndarray or pandas.Series
        The date & time array in a numpy.datetime64 format.
    lat: numpy.ndarray or pandas.Series
        The latitude of the glider position.
    lon: numpy.ndarray or pandas.Series
        The longitude of the glider position.

    Returns
    -------
    sunrise: numpy.ndarray
        An array of the sunrise times.
    sunset: numpy.ndarray
        An array of the sunset times.

    """

    ts = api.load.timescale()
    eph = api.load("de421.bsp")

    df = DataFrame.from_dict(dict([("time", time), ("lat", lat), ("lon", lon)]))

    # set days as index
    df = df.set_index(df.time.values.astype("datetime64[D]"))

    # groupby days and find sunrise/sunset for unique days
    grp_avg = df.groupby(df.index).mean(numeric_only=False)
    date = grp_avg.index

    time_utc = ts.utc(date.year, date.month, date.day, date.hour)
    time_utc_offset = ts.utc(
        date.year, date.month, date.day + 1, date.hour
    )  # add one day for each unique day to compute sunrise and sunset pairs

    bluffton = []
    for i in range(len(grp_avg.lat)):
        bluffton.append(api.wgs84.latlon(grp_avg.lat[i], grp_avg.lon[i]))
    bluffton = np.array(bluffton)

    sunrise = []
    sunset = []
    for n in tqdm(range(len(bluffton))):

        f = almanac.sunrise_sunset(eph, bluffton[n])
        t, y = almanac.find_discrete(time_utc[n], time_utc_offset[n], f)

        if not t:
            if f(time_utc[n]):  # polar day
                sunrise.append(
                    pd.Timestamp(
                        date[n].year, date[n].month, date[n].day, 0, 1
                    ).to_datetime64()
                )
                sunset.append(
                    pd.Timestamp(
                        date[n].year, date[n].month, date[n].day, 23, 59
                    ).to_datetime64()
                )
            else:  # polar night
                sunrise.append(
                    pd.Timestamp(
                        date[n].year, date[n].month, date[n].day, 11, 59
                    ).to_datetime64()
                )
                sunset.append(
                    pd.Timestamp(
                        date[n].year, date[n].month, date[n].day, 12, 1
                    ).to_datetime64()
                )

        else:
            sr = t[y == 1]  # y=1 sunrise
            sn = t[y == 0]  # y=0 sunset

            sunup = pd.to_datetime(sr.utc_iso()).tz_localize(None)
            sundown = pd.to_datetime(sn.utc_iso()).tz_localize(None)

            # this doesn't look very efficient at the moment, but I was having issues with getting the datetime64
            # to be compatible with the above code to handle polar day and polar night

            su = pd.Timestamp(
                sunup.year[0],
                sunup.month[0],
                sunup.day[0],
                sunup.hour[0],
                sunup.minute[0],
            ).to_datetime64()

            sd = pd.Timestamp(
                sundown.year[0],
                sundown.month[0],
                sundown.day[0],
                sundown.hour[0],
                sundown.minute[0],
            ).to_datetime64()

            sunrise.append(su)
            sunset.append(sd)

    sunrise = np.array(sunrise).squeeze()
    sunset = np.array(sunset).squeeze()

    grp_avg["sunrise"] = sunrise
    grp_avg["sunset"] = sunset

    # reindex days to original dataframe as night
    df_reidx = grp_avg.reindex(df.index)
    sunrise, sunset = df_reidx[["sunrise", "sunset"]].values.T

    return sunrise, sunset


def day_night_avg(ds, sel_var='CHLA', start_time=None, end_time=None, start_prof=None, end_prof=None):
    """
    This function computes night and day averages for a selected variable over a specific period of time or a specific series of dives
    Data in divided into day and night using the sunset and sunrise time as described in the above function sunset_sunrise from GliderTools
    Parameters
    ----------
    ds: xarray on OG1 format containing at least time, depth, latitude, longitude and the selected variable. 
        Data should not be gridded.
    sel_var: variable to use to compute the day night averages
    start_time: Start date of the data selection. As missions can be long and can make it hard to visualise NPQ effect,
                we recommend selecting small section of few days to a few weeks. Defaults to the central week of the deployment
    end_time: End date of the data selection. As missions can be long and can make it hard to visualise NPQ effect,
                we recommend selecting small section of few days to a few weeks. Defaults to the central week of the deployment
    start_prof: Start profile of the data selection. If no profile is specified, the specified time selction will be used or the the central week of the deployment.
                It is important to have a large enough number of dives to have some day and night data otherwise the function will not run
    end_prof:  End profile of the data selection. If no profile is specified, the specified time selction will be used or the the central week of the deployment.
            It is important to have a large enough number of dives to have some day and night data otherwise the function will not run
                
    Returns
    -------
    day_av: pandas.Dataframe
        A dataframe with the day averages of the selected variable with the following columns:
            batch: Number representing the grouping for each day. This number can represent the number of the day in chronological order
            depth: Depth values for the average
            dat: Average value for the selected variable
            day: Actual date for the batch 
    night_av: pandas.Dataframe
        A dataframe with the night averages of the selected variable with the following columns:
            batch: Number representing the grouping for each day. This number can represent the number of the day in chronological order
            depth: Depth values for the average
            dat: Average value for the selected variable
            day: Actual date for the batch 

    """
    _necessary_variables_check(ds, ['TIME', sel_var, 'DEPTH'])
    if "TIME" not in ds.indexes.keys():
        ds = ds.set_xindex('TIME')

    if not start_time:
        start_time = ds.TIME.mean() - np.timedelta64(3, 'D')
    if not end_time:
        end_time = ds.TIME.mean() + np.timedelta64(3, 'D')

    if start_prof and end_prof:
        t1 = ds.TIME.where(ds.PROFILE_NUMBER==start_prof).dropna(dim='N_MEASUREMENTS')[0]
        t2 = ds.TIME.where(ds.PROFILE_NUMBER==end_prof).dropna(dim='N_MEASUREMENTS')[-1]
        ds_sel = ds.sel(TIME=slice(t1,t2))
    else:
        ds_sel = ds.sel(TIME=slice(start_time, end_time))
    sunrise, sunset = sunset_sunrise(ds_sel.TIME, ds_sel.LATITUDE, ds_sel.LONGITUDE)

    # creating batches where one batch is a night and the following day
    day = (ds_sel.TIME > sunrise) & (ds_sel.TIME < sunset)
    # find day and night transitions
    daynight_transitions = np.abs(np.diff(day.astype(int)))
    # get the cumulative sum of daynight to generate separate batches for day and night
    daynight_batches = daynight_transitions.cumsum()
    batch = np.r_[0, daynight_batches // 2]

    # Create day and night averages to then have easy to plot
    df = pd.DataFrame(np.c_[ds_sel[sel_var], day, batch, ds_sel['DEPTH']], columns=['dat', 'day', 'batch', 'depth'])
    ave = df.dat.groupby([df.day, df.batch, np.around(df.depth)]).mean()
    day_av = ave[1].to_frame().reset_index()
    night_av = ave[0].to_frame().reset_index()
    #Assign date value

    for i in np.unique(day_av.batch):
        date_val = str(ds_sel.TIME.where(batch == i).dropna(dim='N_MEASUREMENTS')[-1].values)[:10]
        day_av.loc[np.where(day_av.batch == i)[0], 'date'] = date_val
        night_av.loc[np.where(night_av.batch == i)[0], 'date'] = date_val
    return day_av, night_av


def plot_daynight_avg(day: pd.DataFrame, night: pd.DataFrame, ax: plt.Axes = None, sel_day=None,
                      xlabel='Chlorophyll [mg m-3]', **kw: dict, ) -> tuple({plt.Figure, plt.Axes}):
    """
    This function can be used to plot the day and night averages computed with the day_night_avg function
    
    Parameters
    ----------
    day: pandas dataframe containing the day averages
    night: pandas dataframe containing the night averages
    ax: axis to plot the data
    sel_day: selected day to plot. Defaults to the median day
    xlabel: label for the x-axis
    
    Returns
    -------
    A line plot comparing the day and night average over depth for the selected day

    """
    if not sel_day:
        dates = list(day.date.dropna().values) + list(night.date.dropna().values)
        dates.sort()
        sel_day = dates[int(len(dates)/2)]
    if ax is None:
        fig, ax = plt.subplots(figsize=(5, 5))
    else:
        fig = plt.gcf()
    ax.plot(night.where(night.date == sel_day).dropna().dat, night.where(night.date == sel_day).dropna().depth,
            label='Night time average')
    ax.plot(day.where(day.date == sel_day).dropna().dat, day.where(day.date == sel_day).dropna().depth,
            label='Daytime average')
    ax.legend()
    ax.invert_yaxis()
    ax.grid()
    ax.set(xlabel=xlabel, ylabel='Depth [m]')
    ax.set_title(sel_day)
    return fig, ax


def plot_section_with_srss(ds: xr.Dataset, sel_var: str, ax: plt.Axes = None, start_time=None,
                           end_time=None,start_prof=None, end_prof=None, ylim=45, **kw: dict, ) -> tuple({plt.Figure, plt.Axes}):
    """
    This function can be used to plot sections for any variable with the sunrise and sunset plotted over
    
    Parameters
    ----------
    ds: xarray on OG1 format containing at least time, depth, latitude, longitude and the selected variable. 
        Data should not be gridded.
    sel_var: selected variable to plot
    ax: axis to plot the data
    start_time: Start date of the data selection format 'YYYY-MM-DD'. As missions can be long and came make it hard to visualise NPQ effect. Defaults to mid 4 days
    end_time: End date of the data selection format 'YYYY-MM-DD'. As missions can be long and came make it hard to visualise NPQ effect. Defaults to mid 4 days
    start_prof: Start profile of the data selection. If no profile is specified, the specified time selction will be used or the mid 4 days of the deployment
    end_prof:  End profile of the data selection. If no profile is specified, the specified time selction will be used or the mid 4 days of the deployment
    ylim: specified limit for the maximum y-axis value. The minimum is computed as ylim/30
    
    Returns
    -------
    A section showing the variability of the selected data over time and depth
    """
    _necessary_variables_check(ds, ['TIME', sel_var, 'DEPTH'])
    if ax is None:
        fig, ax = plt.subplots(figsize=(5, 5))
    else:
        fig = plt.gcf()

    if "TIME" not in ds.indexes.keys():
        ds = ds.set_xindex('TIME')
    
    if not start_time:
        start_time = ds.TIME.mean() - np.timedelta64(2, 'D')
    if not end_time:
        end_time = ds.TIME.mean() + np.timedelta64(2, 'D')
    
    if start_prof and end_prof:
        t1 = ds.TIME.where(ds.PROFILE_NUMBER==start_prof).dropna(dim='N_MEASUREMENTS')[0]
        t2 = ds.TIME.where(ds.PROFILE_NUMBER==end_prof).dropna(dim='N_MEASUREMENTS')[-1]
        ds_sel = ds.sel(TIME=slice(t1,t2))
    else:
        ds_sel = ds.sel(TIME=slice(start_time, end_time))
    
    if len(ds_sel.TIME) == 0:
        msg = f"supplied limits start_time: {start_time} end_time: {end_time} do not overlap with dataset TIME range {str(ds.TIME.values.min())[:10]} - {str(ds.TIME.values.max())[:10]}"
        raise ValueError(msg)
    
    sunrise, sunset = sunset_sunrise(ds_sel.TIME, ds_sel.LATITUDE, ds_sel.LONGITUDE)

    c = ax.scatter(ds_sel.TIME, ds_sel.DEPTH, c=ds_sel[sel_var], s=10, vmin=np.nanpercentile(ds_sel[sel_var], 0.5),
                   vmax=np.nanpercentile(ds_sel[sel_var], 99.5))
    ax.set_ylim(ylim, -ylim / 30)
    for n in np.unique(sunset):
        ax.axvline(np.unique(n), c='blue')
    for m in np.unique(sunrise):
        ax.axvline(np.unique(m), c='orange')
    ax.set_ylabel('Depth [m]')
    plt.colorbar(c, label=f'{sel_var} [{ds[sel_var].units}]')
    return fig, ax


def check_temporal_drift(ds: xr.Dataset, var: str, ax: plt.Axes = None, **kw: dict, ) -> tuple({plt.Figure, plt.Axes}):
    _necessary_variables_check(ds, ['TIME', var, 'DEPTH'])
    if ax is None:
        fig, ax = plt.subplots(1, 2, figsize=(14, 6))
    else:
        fig = plt.gcf()

    if var not in ds.variables:
        print(f'{var} does not exist in the dataset. Make sure the spelling is correct or add this variable to your dataset')
    else:
        ax[0].scatter(mdates.date2num(ds.TIME), ds[var], s=10)
        ax[0].xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
        ax[0].set(ylim=(np.nanpercentile(ds[var], 0.01), np.nanpercentile(ds[var], 99.99)), ylabel=var)

        c = ax[1].scatter(ds[var], ds.DEPTH, c=mdates.date2num(ds.TIME), s=10)
        ax[1].set(xlim=(np.nanpercentile(ds[var], 0.01), np.nanpercentile(ds[var], 99.99)), ylabel='Depth (m)', xlabel=var)
        ax[1].invert_yaxis()

        [a.grid() for a in ax]
        plt.colorbar(c, format=DateFormatter('%b %d'))
    return fig, ax


def check_monotony(da):
    """
    This function check weather the selected variable over the mission is monotonically increasing or not. This is developed in particular for profile number.
    If the profile number is not monotonically increasing, this may mean that whatever function was used to assign the profile number may have misassigned some points.
    
    Parameters
    ----------
    da: xarray.DataArray on OG1 format. Data should not be gridded.

    Returns
    -------
    It will print a sentence stating whether data is

    """
    if not pd.Series(da).is_monotonic_increasing:
        print(f'{da.name} is not always monotonically increasing')
        return False
    else:
        print(f'{da.name} is always monotonically increasing')
        return True


def plot_profIncrease(ds: xr.DataArray, ax: plt.Axes = None, **kw: dict, ) -> tuple({plt.Figure, plt.Axes}):
    """
    This function can be used to plot the profile number and check for any possible issues with the profile index assigned.

    Parameters
    ----------
    ds: xarray in OG1 format with at least PROFILE_NUMBER, TIME, DEPTH. Data should not be gridded
    ax: axis to plot the data

    Returns -------
    Two plots, one line plot with the profile number over time (expected to be always increasing). A
    second plot which is a scatter plot showing at which depth over time there was a profile index where the
    difference was neither 0 nor 1 (meaning there are possibly issues with how the profile index was assigned)

    """
    _necessary_variables_check(ds, ['TIME', 'PROFILE_NUMBER', 'DEPTH'])
    if ax is None:
        fig, ax = plt.subplots(2, 1, figsize=(10, 5), sharex=True)
    else:
        fig = plt.gcf()

    ax[0].plot(ds.TIME, ds.PROFILE_NUMBER)
    ax[0].set(ylabel='Profile_Number')
    if len(np.where((np.diff(ds.PROFILE_NUMBER) != 0) & (np.diff(ds.PROFILE_NUMBER) != 1))[0]) == 0:
        ax[1].text(0.2, 0.5, 'Data in monotonically increasing and no issues can be observed',
                   transform=ax[1].transAxes)
    else:
        ax[1].scatter(ds.TIME[np.where((np.diff(ds.PROFILE_NUMBER) != 0) & (np.diff(ds.PROFILE_NUMBER) != 1))],
                      ds.DEPTH[np.where((np.diff(ds.PROFILE_NUMBER) != 0) & (np.diff(ds.PROFILE_NUMBER) != 1))],
                      s=10, c='red', label='Depth at which we have issues \n with the profile number assigned')
    ax[1].set(ylabel='Depth')
    ax[1].invert_yaxis()
    ax[1].legend()
    ax[1].xaxis.set_major_locator(plt.MaxNLocator(8))
    [a.grid() for a in ax]
    return fig, ax


def plot_glider_track(ds: xr.Dataset, ax: plt.Axes = None, **kw: dict) -> tuple({plt.Figure, plt.Axes}):
    """
    This function plots the glider track on a map, with latitude and longitude colored by time.

    Parameters
    ----------
    ds: xarray in OG1 format with at least TIME, LATITUDE, and LONGITUDE.
    ax: Optional; axis to plot the data.
    kw: Optional; additional keyword arguments for the scatter plot.

    Returns
    -------
    One plot with the map of the glider track.
    fig: matplotlib.figure.Figure
    ax: matplotlib.axes._subplots.AxesSubplot
    """
    _necessary_variables_check(ds, ['TIME', 'LONGITUDE', 'LATITUDE'])
    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 6), subplot_kw={'projection': ccrs.PlateCarree()})
    else:
        fig = plt.gcf()

    latitudes = ds.LATITUDE.values
    longitudes = ds.LONGITUDE.values
    times = ds.TIME.values

    # Reduce the number of latitudes, longitudes, and times to no more than 2000
    if len(latitudes) > 2000:
        indices = np.linspace(0, len(latitudes) - 1, 2000).astype(int)
        latitudes = latitudes[indices]
        longitudes = longitudes[indices]
        times = times[indices]

    # Convert time to the desired format
    time_labels = [pd.to_datetime(t).strftime('%Y-%b-%d') for t in times]
    
    # Plot latitude and longitude colored by time
    sc = ax.scatter(longitudes, latitudes, c=times, cmap='viridis', **kw)
    
    # Add colorbar with formatted time labels
    cbar = plt.colorbar(sc, ax=ax) #, label='Time')
    cbar.ax.set_yticklabels([pd.to_datetime(t).strftime('%Y-%b-%d') for t in cbar.get_ticks()])

    ax.set_extent([np.min(longitudes)-1, np.max(longitudes)+1, np.min(latitudes)-1, np.max(latitudes)+1], crs=ccrs.PlateCarree())

    # Add features to the map
    ax.add_feature(cfeature.LAND)
    ax.add_feature(cfeature.OCEAN)
    ax.add_feature(cfeature.COASTLINE)

    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    ax.set_title('Glider Track')
    gl = ax.gridlines(draw_labels=True, color='black', alpha=0.5, linestyle='--')
    gl.top_labels = False
    gl.right_labels = False
    plt.show()

    return fig, ax

def plot_grid_spacing_histograms(ds: xr.Dataset, ax: plt.Axes = None, **kw: dict) -> tuple({plt.Figure, plt.Axes}):
    """
    This function plots histograms of the grid spacing (diff(ds.DEPTH) and diff(ds.TIME)) where only the inner 99% of values are plotted.

    Parameters
    ----------
    ds: xarray in OG1 format with at least TIME and DEPTH.
    ax: Optional; axis to plot the data.
    kw: Optional; additional keyword arguments for the histograms.

    Returns
    -------
    Two histograms showing the distribution of grid spacing for depth and time.
    fig: matplotlib.figure.Figure
    ax: matplotlib.axes._subplots.AxesSubplot
    """
    _necessary_variables_check(ds, ['TIME', 'DEPTH'])
    if ax is None:
        fig, ax = plt.subplots(1, 2, figsize=(14, 6))
    else:
        fig = plt.gcf()

    depth_diff = np.diff(ds.DEPTH)
    orig_time_diff = np.diff(ds.TIME) / np.timedelta64(1, 's')  # Convert to seconds

    depth_diff = depth_diff[np.isfinite(depth_diff)]
    time_diff = orig_time_diff[np.isfinite(orig_time_diff)]

    depth_diff = depth_diff[(depth_diff >= np.nanpercentile(depth_diff, 0.5)) & (depth_diff <= np.nanpercentile(depth_diff, 99.5))]
    time_diff = time_diff[(time_diff >= np.nanpercentile(time_diff, 0.5)) & (time_diff <= np.nanpercentile(time_diff, 99.5))]

    ax[0].hist(depth_diff, bins=50, **kw)
    ax[0].set_xlabel('Depth Spacing (m)')
    ax[0].set_ylabel('Frequency')
    ax[0].set_title('Histogram of Depth Spacing')
    ax[0].grid()

    median_neg_depth_diff = np.median(depth_diff[depth_diff < 0])
    median_pos_depth_diff = np.median(depth_diff[depth_diff > 0])
    max_depth_diff = np.max(depth_diff)
    min_depth_diff = np.min(depth_diff)

    annotation_text_left = (
        f'Median Negative: {median_neg_depth_diff:.2f} m\n'
        f'Median Positive: {median_pos_depth_diff:.2f} m\n'
        f'Max: {max_depth_diff:.2f} m\n'
        f'Min: {min_depth_diff:.2f} m'
    )
    ax[0].annotate(annotation_text_left, xy=(0.96, 0.96), xycoords='axes fraction', 
                   fontsize=12, ha='right', va='top', 
                   bbox=dict(boxstyle='round,pad=0.3', edgecolor='black', facecolor='white', alpha=.5))

    ax[1].hist(time_diff, bins=50, **kw)
    ax[1].set_xlabel('Time Spacing (s)')
    ax[1].set_ylabel('Frequency')
    ax[1].set_title('Histogram of Time Spacing')
    ax[1].grid()

    median_time_diff = np.median(orig_time_diff)
    mean_time_diff = np.mean(orig_time_diff)
    max_time_diff = np.max(orig_time_diff)
    min_time_diff = np.min(orig_time_diff)
    max_time_diff_hrs = max_time_diff/3600

    annotation_text = (
        f'Median: {median_time_diff:.2f} s\n'
        f'Mean: {mean_time_diff:.2f} s\n'
        f'Max: {max_time_diff:.2f} s ({max_time_diff_hrs:.2f} hr)\n'
        f'Min: {min_time_diff:.2f} s'
    )
    ax[1].annotate(annotation_text, xy=(0.96, 0.96), xycoords='axes fraction', 
                    fontsize=12, ha='right', va='top', 
                    bbox=dict(boxstyle='round,pad=0.3', edgecolor='black', facecolor='white', alpha=.5))

    return fig, ax

def plot_ts_histograms(ds: xr.Dataset, ax: plt.Axes = None, **kw: dict) -> tuple({plt.Figure, plt.Axes}):
    """
    This function plots histograms of temperature and salinity values (middle 95%), and a 2D histogram of salinity and temperature with density contours.

    Parameters
    ----------
    ds: xarray in OG1 format with at least TEMP and PSAL.
    ax: Optional; axis to plot the data.
    kw: Optional; additional keyword arguments for the histograms.

    Returns
    -------
    Three plots: histogram of temperature, histogram of salinity, and 2D histogram of salinity and temperature with density contours.
    fig: matplotlib.figure.Figure
    ax: matplotlib.axes._subplots.AxesSubplot
    """
    _necessary_variables_check(ds, ['DEPTH', 'LONGITUDE', 'LATITUDE', 'PSAL', 'TEMP'])

    if ax is None:
        fig, ax = plt.subplots(1, 3, figsize=(18, 6))
    else:
        fig = plt.gcf()

    temp_orig = ds.TEMP.values
    sal_orig = ds.PSAL.values

    # Reduce both to where both are finite
    temp = temp_orig[np.isfinite(temp_orig)&np.isfinite(sal_orig)]
    sal = sal_orig[np.isfinite(sal_orig)&np.isfinite(temp_orig)]
    depth = ds.DEPTH[np.isfinite(sal_orig)&np.isfinite(temp_orig)]
    long = ds.LONGITUDE[np.isfinite(sal_orig)&np.isfinite(temp_orig)]
    lat = ds.LATITUDE[np.isfinite(sal_orig)&np.isfinite(temp_orig)]

    SA = gsw.SA_from_SP(sal, depth, long, lat)
    CT = gsw.CT_from_t(SA, temp, depth)

    # Reduce to middle 95% of values
    temp_filtered = CT[(CT >= np.nanpercentile(CT, 2.5)) & (CT <= np.nanpercentile(CT, 97.5))]
    sal_filtered = SA[(SA >= np.nanpercentile(SA, 2.5)) & (SA <= np.nanpercentile(SA, 97.5))]

    ax[0].hist(temp_filtered, bins=50, **kw)
    ax[0].set_xlabel('Conservative Temperature (°C)')
    ax[0].set_ylabel('Frequency')
    ax[0].set_title('Histogram of Temperature')
    ax[0].grid()

    ax[1].hist(sal_filtered, bins=50, **kw)
    ax[1].set_xlabel('Absolute Salinity ( )')
    ax[1].set_ylabel('Frequency')
    ax[1].set_title('Histogram of Salinity')
    ax[1].grid()

    h = ax[2].hist2d(sal, temp, bins=50, cmap='viridis', norm=mcolors.LogNorm(), **kw)
    cbar = plt.colorbar(h[3], ax=ax[2])
    cbar.set_label('Log Counts')
    ax[2].set_xlabel('Absolute Salinity ( )')
    ax[2].set_ylabel('Conservative Temperature (°C)')
    ax[2].set_title('2D Histogram of Salinity and Temperature (Log Scale)')

    # Calculate density and add contours
    SA = gsw.SA_from_SP(sal, depth, long, lat)
    CT = gsw.CT_from_t(SA, temp, depth)
    sigma0 = gsw.sigma0(SA, CT)

    xi = np.linspace(sal.min()-1, sal.max()+1, 100)
    yi = np.linspace(temp.min()-1, temp.max()+1, 100)
    xi, yi = np.meshgrid(xi, yi)
    zi = gsw.sigma0(xi, yi)

    ax[2].contour(xi, yi, zi, colors='black', alpha=0.5, linewidths=0.5)
    ax[2].clabel(ax[2].contour(xi, yi, zi, colors='black', alpha=0.5, linewidths=0.5), inline=True, fontsize=10)

    return fig, ax


def calc_DEPTH_Z(ds):
    """
    Calculate the depth (Z position) of the glider using the gsw library to convert pressure to depth.
    
    Parameters
    ----------
    ds (xarray.Dataset): The input dataset containing 'PRES', 'LATITUDE', and 'LONGITUDE' variables.
    
    Returns
    -------
    xarray.Dataset: The dataset with an additional 'DEPTH_Z' variable.
    """
    # Ensure the required variables are present
    if 'PRES' not in ds.variables or 'LATITUDE' not in ds.variables or 'LONGITUDE' not in ds.variables:
        raise ValueError("Dataset must contain 'PRES', 'LATITUDE', and 'LONGITUDE' variables.")

    # Initialize the new variable with the same dimensions as dive_num
    ds['DEPTH_Z'] = (['N_MEASUREMENTS'], np.full(ds.dims['N_MEASUREMENTS'], np.nan))

    # Calculate depth using gsw
    depth = gsw.z_from_p(ds['PRES'], ds['LATITUDE'])
    ds['DEPTH_Z'] = depth

    # Assign the calculated depth to a new variable in the dataset
    ds['DEPTH_Z'].attrs = {
        "units": "meters",
        "positive": "up",
        "standard_name": "depth",
        "comment": "Depth calculated from pressure using gsw library, positive up.",
    }
    
    return ds

def calc_glider_w_from_depth(ds):
    """
    Calculate the vertical velocity of a glider using changes in pressure with time.

    Parameters
    ----------
    ds (xarray.Dataset): Dataset containing 'DEPTH' and 'TIME'.
    - DEPTH (array-like): Array of depth measurements
    - TIME (array-like): Array of time stamps
    
    Returns
    -------
    ds (xarray.Dataset): Containing the new variable
    - GLIDER_VERT_VELO_DZDT (array-like): with vertical velocities calculated from dz/dt
    """
    # Ensure inputs are numpy arrays
    time = ds.TIME.values
    if 'DEPTH_Z' not in ds.variables and all(var in ds.variables for var in ['PRES', 'LATITUDE', 'LONGITUDE']):
        ds = calc_DEPTH_Z(ds)
    depth = ds.DEPTH_Z.values

    # Calculate the centered differences in pressure and time, i.e. instead of using neighboring points, 
    # use the points two steps away.  This has a couple of advantages: one being a slight smoothing of the
    # differences, and the other that the calculated speed will be the speed at the midpoint of the two 
    # points.
    # For data which are evenly spaced in time, this will be equivalent to a centered difference.
    # For data which are not evenly spaced in time, i.e. when a Seaglider sample rate changes from 5 
    # seconds to 10 seconds, there may be some uneven weighting of the differences.
    delta_z_meters = (depth[2:] - depth[:-2]) 
    delta_time_datetime64ns = (time[2:] - time[:-2]) 
    delta_time_sec = delta_time_datetime64ns / np.timedelta64(1, 's')  # Convert to seconds

    # Calculate vertical velocity (rate of change of pressure with time)
    vertical_velocity = delta_z_meters / delta_time_sec

    # Pad the result to match the original array length
    vertical_velocity = np.pad(vertical_velocity, (1, 1), 'edge') 

    # No - Convert vertical velocity from m/s to cm/s
    vertical_velocity = vertical_velocity 

    # Add vertical velocity to the dataset
    ds = ds.assign(GLIDER_VERT_VELO_DZDT=(('N_MEASUREMENTS'), vertical_velocity,  {'long_name': 'glider_vertical_speed_from_pressure', 'units': 'm s-1'}))

    return ds

def calc_seawater_w(ds):
    """
    Calculate the vertical seawater velocity and add it to the dataset.

    Parameters
    ----------
    ds (xarray.Dataset): Dataset containing 'VERT_GLIDER_SPEED' and 'VERT_SPEED_DZDT'.

    Returns
    -------
    ds (xarray.Dataset): Dataset with the new variable 'VERT_SW_SPEED', which is the inferred vertical seawater velocity.

    Eleanor's note: This could be bundled with calc_glider_w_from_depth, but keeping them separate allows for some extra testing/flexibility for the user. 
    """
    # Check if 'VERT_GLIDER_SPEED' is in the dataset
    if 'GLIDER_VERT_VELO_MODEL' not in ds:
        print("Error: 'GLIDER_VERT_VELO_MODEL' is not in the dataset.")
        return ds

    # Calculate the vertical seawater velocity
    vert_sw_speed = ds['GLIDER_VERT_VELO_DZDT'].values - ds['GLIDER_VERT_VELO_MODEL'].values 

    # Add vertical seawater velocity to the dataset as a data variable
    ds = ds.assign(VERT_CURR_MODEL=(('N_MEASUREMENTS'), vert_sw_speed, {'long_name': 'vertical_current_of_seawater_derived_from_glider_flight_model', 'units': 'm s-1'}))
    return ds


def plot_vertical_speeds_with_histograms(ds, start_prof=None, end_prof=None):
    """
    Plot vertical speeds with histograms for diagnostic purposes.
    This function generates a diagnostic plot for the calculation of vertical seawater velocity.
    It plots the modelled and computed (from dz/dt) vertical velocities as line plots, where these
    should be similar. The difference between these velocities is the implied seawater velocity,
    which should be closer to zero than the vehicle velocities. The histogram provides a visual
    representation to identify any biases. The final calculation of the median should be close to
    zero if a large enough sample of dives is input and if the glider flight model is well-tuned.

    Parameters
    ----------
    ds (xarray.Dataset): The dataset containing the vertical speed data where
    - VERT_GLIDER_SPEED is the modelled glider speed
    - VERT_SPEED_DZDT is the computed glider speed from the pressure sensor
    - VERT_SW_SPEED is the implied seawater velocity.
    start_prof (int, optional): The starting profile number for subsetting the dataset. Defaults to first profile number.
    end_prof (int, optional): The ending profile number for subsetting the dataset. Defaults to last profile number.

    Returns
    -------
    fig, axs (tuple): The figure and axes objects for the plot.
    """
    required_vars = ['GLIDER_VERT_VELO_MODEL', 'GLIDER_VERT_VELO_DZDT', 'VERT_CURR_MODEL']
    for var in required_vars:
        if var not in ds:
            print(f"Dataset must contain '{var}' to create this plot.")
            return

    if start_prof is not None and end_prof is not None:
        # Subset the dataset for the given profile range
        ds = ds.where((ds['PROFILE_NUMBER'] >= start_prof) & (ds['PROFILE_NUMBER'] <= end_prof), drop=True)

    if start_prof is None:
        start_prof = ds['PROFILE_NUMBER'].values.min()
    
    if end_prof is None:
        end_prof = ds['PROFILE_NUMBER'].values.max() 

    vert_curr = ds.VERT_CURR_MODEL.values * 100  # Convert to cm/s
    vert_dzdt = ds.GLIDER_VERT_VELO_DZDT.values * 100  # Convert to cm/s
    vert_model = ds.GLIDER_VERT_VELO_MODEL.values * 100  # Convert to cm/s


    fig, axs = plt.subplots(2, 2, figsize=(14, 12), gridspec_kw={'width_ratios': [3, 1]})

    # Upper left subplot for vertical velocity and glider speed
    ax1 = axs[0, 0]
    ax1.plot(ds['TIME'], vert_dzdt, label='Vertical Velocity (from dz/dt)')
    ax1.set_xlabel('Time')
    ax1.set_ylabel('Vertical Velocity (cm/s)')
    ax1.legend(loc='lower left')

    ax1_twin = ax1.twinx()
    ax1_twin.plot(ds['TIME'], vert_model, color='r', label='Vertical Glider Speed (model)')
    ax1_twin.legend(loc='lower left')

    ax1_twin.plot(ds['TIME'], vert_curr, color='g', label='Vertical Water Speed (calculated)')
    ax1_twin.legend(loc='lower right')
    # Remove y-axis labels on the right
    ax1_twin.set_yticklabels([])

    # Upper right subplot for histogram of vertical velocity
    ax1_hist = axs[0, 1]
    ax1_hist.hist(vert_dzdt, bins=50, orientation='horizontal', alpha=0.5, color='blue', label='Vertical Velocity (from dz/dt)')
    ax1_hist.hist(vert_model, bins=50, orientation='horizontal', alpha=0.5, color='red', label='Vertical Glider Speed (model)')
    ax1_hist.hist(vert_curr, bins=50, orientation='horizontal', alpha=0.5, color='green', label='Vertical Water Speed (calculated)')
    ax1_hist.set_xlabel('Frequency')

    # Determine the best location for the legend based on the y-axis limits and zero
    y_upper_limit = ax1_hist.get_ylim()[1]
    y_lower_limit = ax1_hist.get_ylim()[0]

    if abs(y_upper_limit) > abs(y_lower_limit):
        legend_loc = 'upper right'
    else:
        legend_loc = 'lower right'

    ax1_hist.legend(loc=legend_loc)

    # Lower left subplot for vertical water speed
    ax2 = axs[1, 0]
    ax2.axhline(0, color='darkgray', linestyle='-', linewidth=0.5)  # Add zero horizontal line
    ax2.plot(ds['TIME'], vert_curr, 'g', label='Vertical Water Speed')
    ax2.set_xlabel('Time')
    ax2.set_ylabel('Vertical Water Speed (cm/s)')
    ax2.legend(loc='upper left')

    # Lower right subplot for histogram of vertical water speed
    ax2_hist = axs[1, 1]
    ax2_hist.hist(vert_curr, bins=50, orientation='horizontal', alpha=0.5, color='green', label='Vertical Water Speed (calculated)')
    ax2_hist.set_xlabel('Frequency')

    # Calculate and plot the median line
    median_vert_sw_speed = np.nanmedian(vert_curr)
    ax2_hist.axhline(median_vert_sw_speed, color='red', linestyle='dashed', linewidth=1, label=f'Median: {median_vert_sw_speed:.2f} cm/s')

    # Determine the best location for the legend based on the y-axis limits and median
    y_upper_limit = ax2_hist.get_ylim()[1]
    y_lower_limit = ax2_hist.get_ylim()[0]
    median_vert_sw_speed = np.nanmedian(vert_curr)

    if abs(y_upper_limit - median_vert_sw_speed) > abs(y_lower_limit - median_vert_sw_speed):
        legend_loc = 'upper right'
    else:
        legend_loc = 'lower right'

    ax2_hist.legend(loc=legend_loc)

    plt.tight_layout()
    plt.show()

    return fig, axs
