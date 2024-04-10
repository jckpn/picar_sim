
### idea 1: 'director' and 'driver' (?)
- maybe there's a proper name for this idk
- two models:
	1. director model
		- big-ish model (camera view or bounding boxes as input)
		- outputs a target point, where the picar needs to drive to
		- or removes target point if picar needs to stop
	2. driver model
		- small model
		- takes target point (2D co-ord) and smoothly drives towards it
		- once target point is reached the director model should hopefully have made another inference

### idea 2: MoE
- train different 'expert' models for each scenario
	- e.g. one for oval, one for junction, one for intersection
	- one for left turn at junction, one for right turn at junction, etc.
	- can potentially train the experts using 2D sim and fine-tune them in real life
- each expert model could probably be quite small
	- so quicker inference time $\to$ smoother driving
	- since much less to consider per scenario vs for all scenarios
- gating model recognises which scenario (test) is taking place and switches model weights accordingly
- gating model can override expert e.g. if obstacle in way or red light
- this would improve performance in some areas

### idea 3: reinforcement learning with 2D sim
- train CNN to detect bounding boxes of road and obstacles
- convert them to 2D
- reinforcement learning (q-learning or neuroevolution etc.) to learn how to drive and complete courses with given obstacles as state