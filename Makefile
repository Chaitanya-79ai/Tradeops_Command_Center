.PHONY: docker-up docker-down premarket monitor backend dashboard


docker-up:
	docker compose up --build


docker-down:
	docker compose down


premarket:
	./scripts/premarket_check.sh


monitor:
	python3 -m monitor.monitor


backend:
	python3 -m uvicorn backend.main:app --port 8000 --reload


dashboard:
	streamlit run dashboard/app.py
