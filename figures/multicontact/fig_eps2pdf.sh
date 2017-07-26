#!/bin/bash

cd ../data
gnuplot plot_figures_eps.gnu

cd ../figures
epspdf contacts.eps 
epspdf com.eps
epspdf lf_forces.eps
epspdf rf_forces.eps
epspdf rh_forces.eps

exit 0

