Workflow
	1.	Develop Locally First:
	•	Use a minimal loop: Flask to trigger tick_pipeline.py manually
	•	Streamlit reads JSON state
	2.	Add CrewAI Agents:
	•	Define tools + memories
	•	Let central_ai.py orchestrate goals
	3.	Wrap Kubeflow Pipelines:
	•	Each step/*.py becomes a pipeline component
	•	Use kfp.components.create_component_from_func
	4.	Deploy to EKS:
	•	Helm to manage deployment
	•	Store persistent game state in DynamoDB