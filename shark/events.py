'''Finds events in a light curve and quantifies them.
'''

import numpy as np

def group_consecutives(vals, step=1):
    """Return list of consecutive lists of numbers from vals (number list)."""
    run = []
    result = [run]
    expect = None
    for v in vals:
        if (v == expect) or (expect is None):
            run.append(v)
        else:
            run = [v]
            result.append(run)
        expect = v + step
    return result


def find_events(x,y,threshold=0.2,med=None,return_groups=False, n=3):
    '''
    Finds the groups of points that are below a certain threshold. Groups must consist of at least 3 points. This is an old code and could be improved.
    '''
    if med==None:
        med=np.nanmedian(y)

    dt = np.median(x[1:]-x[:-1])
    mask = np.abs(y-med) <= (threshold)
    np_s = len(np.where(mask == False)[0])
    groups = group_consecutives(np.where(mask == False)[0])

    grouplen = [len(g) for g in groups]
    ngroup = len(np.where(np.asarray(grouplen) >= n)[0])

    if return_groups==True:
        groups1 = groups
        groups1 = [x for x in groups1 if len(x) >= n]
        return groups1

    if ngroup >= 1:
        group_ind = [np.where(np.asarray(grouplen) >= n)][0][0]
        groupmed = np.median(np.asarray(grouplen)[group_ind])
        dips=[]
        h=[]
        l=[]
        for g in group_ind:
            if np.max((y[groups[g]]-med))<0:
                continue
            h.append(np.max((y[groups[g]]-med)))
            l.append(x[groups[g]][-1]-x[groups[g]][0])
            for i in groups[g]:
                dips.append(i)
    else:
        dict={'ngroups':0,
            'duty':0,
            'medh':0,
            'medh_top':0,
            'dh':0,
            'medl':0,
            'dl':0,
            'dips':0,
        }
        return dict


    if len(h)==0:
        dict={'ngroups':0,
            'duty':0,
            'medh':0,
            'medh_top':0,
            'dh':0,
            'medl':0,
            'dl':0,
            'dips':0,
        }
        return dict

    medh = np.median(h)
    h2 = np.flipud(np.sort(h))
    if len(h2) >= 5:
        medh_top = (np.mean(h2[0:5]))
    else:
        try:
            medh_top = medh
        except:
            medh_top = 0

    duty=np.float(len(dips))/np.float(len(x))
    dict={'ngroups':ngroup,
            'duty':duty,
            'medh':medh,
            'medh_top':medh_top,
            'dh':np.max(h)-np.min(h),
            'medl':np.median(l),
            'dl':np.max(l)-np.min(l),
            'dips':dips,
            'h':h,
            'l':l
    }
    return dict
