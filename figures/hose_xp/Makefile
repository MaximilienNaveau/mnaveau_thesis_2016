# convert the list of .eps in pdf
PDFFILE=yaw_drift_simGraph.pdf

all: ${PDFFILE}

${PDFFILE}: yaw_drift_simGraph.eps
	epspdf coordinates.eps
	epspdf experiment_noController.eps
	epspdf exp_pos.eps
	epspdf Hose_HRP2.eps
	epspdf sim_pos.eps
	epspdf yaw_drift.eps
	epspdf yaw_drift_graph.eps
	epspdf yaw_drifts_3weights.eps
	epspdf yaw_drift_sim.eps
	epspdf yaw_drift_simGraph.eps
	epspdf force_Z_feet_withController_zoomEnd.eps
	epspdf force_Z_feet_withoutController_zoomEnd.eps



clean :
	rm experiment_noController.pdf
	rm exp_pos.pdf
	rm Hose_HRP2.pdf
	rm sim_pos.pdf
	rm yaw_drift.pdf
	rm yaw_drift_graph.pdf
	rm yaw_drifts_3weights.pdf
	rm yaw_drift_sim.pdf
	rm yaw_drift_simGraph.pdf
	rm force_Z_feet_withController_zoomEnd.pdf
	rm force_Z_feet_withoutController_zoomEnd.pdf

# dummy targets
.PHONY: clean
