#--- Legacy python 2.7
from __future__ import division
from __future__ import print_function
# --- General
import unittest
import numpy as np
# --- Local

from vortexcylinder.WindTurbine import WindTurbine
from vortexcylinder.Solver import Ct_const_cutoff

# --------------------------------------------------------------------------------}
import matplotlib.pyplot as plt

def main():
    R=65
    h_hub=0

    r_bar_cut = 0.11
    r_bar_tip = 0.90
    CT0       = 0.80
    Lambda    = 6
    U0        = 10
    R         = 65
    nCyl  = 15
    root  = False
    longi = False
    tang  = True 

    WT=WindTurbine(R=R,e_shaft_yaw0=[0,0,1],e_vert=[0,1,0])
    wd=0 # Wind direction
    #YE=np.linspace(-np.pi/6,np.pi/6,3) # Yaw Error
    YE=[0]

    vr_bar    = np.linspace(0,1.0,100)
    Ct_AD     = Ct_const_cutoff(CT0,r_bar_cut,vr_bar,r_bar_tip) # TODO change me
    WT.update_loading(r=vr_bar*R, Ct=Ct_AD, Lambda=Lambda, nCyl=nCyl)


    for ye in YE:
        WT.update_yaw_pos( wd-ye)
        WT.update_wind([10*np.sin(wd),0,10*np.cos(wd)])

        # --- Flow field and speed
        nx=50
        nz=51
        x = np.linspace(-4*R,4*R,nx)
        z = np.linspace(-4*R,4*R,nz)
        [X,Z]=np.meshgrid(x,z)
        Y=Z*0+h_hub
        ux,uy,uz = WT.compute_u(X,Y,Z,root=root,longi=longi,tang=tang,no_wake=True,only_ind=True)

        fig=plt.figure()
        ax=fig.add_subplot(111)
        Speed=np.sqrt(uz**2+ux**2)
        im=ax.contourf(Z/R,X/R,Speed,levels=30)
        Rotor=WT.rotor_disk_points()
        ax.plot(Rotor[2,:]/R,Rotor[0,:]/R,'k--')
        cb=fig.colorbar(im)
        sp=ax.streamplot(z/R,x/R,uz.T,ux.T,color='k',linewidth=0.7,density=2)
        ax.set_xlabel('z/R [-]')
        ax.set_ylabel('x/R [-]')
        deg=180/np.pi
        ax.set_title('yaw_pos = {:.1f} - yaw_wind={:.1f} - chi={:.1f} - yaw_err={:.1f}'.format(WT.yaw_pos*deg,WT.yaw_wind*deg,WT.chi*deg,WT.yaw_error*deg))
        plt.show()

if __name__ == "__main__":
    main()
#     unittest.main()
