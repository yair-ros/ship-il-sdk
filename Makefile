.PHONY: install lint test format check-black check-flake8 example-getclosestpoints example-insertpickupshipmentex example-get-wb-thermal-or-a4-for-print

VENV_ACTIVATE = source ./.venv/bin/activate
VENV_BIN = ./.venv/bin

install:
	@echo "📦 Installing development tools..."
	$(VENV_BIN)/pip install black flake8 pytest

check-black:
	@test -x $(VENV_BIN)/black || { \
		echo "🔍 'black' not found, running 'make install'..."; \
		$(MAKE) install; \
	}

check-flake8:
	@test -x $(VENV_BIN)/flake8 || { \
		echo "🔍 'flake8' not found, running 'make install'..."; \
		$(MAKE) install; \
	}

lint: check-flake8
	@echo "✅ Running flake8..."
	$(VENV_BIN)/flake8 src

test:
	@echo "✅ Running pytest..."
	PYTHONPATH=src $(VENV_BIN)/pytest -q

format: check-black
	@echo "✅ Running black..."
	$(VENV_BIN)/black src

example-getclosestpoints:
	@test -n "$(SHIP_API_USER)" || (echo "Missing SHIP_API_USER" && exit 1)
	@test -n "$(SHIP_API_PASSWORD)" || (echo "Missing SHIP_API_PASSWORD" && exit 1)
	@test -n "$(SHIP_CUSTOMER_ID)" || (echo "Missing SHIP_CUSTOMER_ID" && exit 1)
	@echo "🚀 Running closest-points example..."
	PYTHONPATH=src SHIP_API_USER="$(SHIP_API_USER)" SHIP_API_PASSWORD="$(SHIP_API_PASSWORD)" SHIP_CUSTOMER_ID="$(SHIP_CUSTOMER_ID)" SHIP_ENV="$(or $(SHIP_ENV),DEV)" SHIP_CITY="$(or $(SHIP_CITY),Tel Aviv)" SHIP_STREET="$(or $(SHIP_STREET),Herzl)" SHIP_HOUSE_NUMBER="$(or $(SHIP_HOUSE_NUMBER),10)" SHIP_POINT_TYPES="$(or $(SHIP_POINT_TYPES),1,2,4)" SHIP_POINTS_LIMIT="$(or $(SHIP_POINTS_LIMIT),10)" $(VENV_BIN)/python examples/getclosestpoints.py

example-insertpickupshipmentex:
	@test -n "$(SHIP_API_USER)" || (echo "Missing SHIP_API_USER" && exit 1)
	@test -n "$(SHIP_API_PASSWORD)" || (echo "Missing SHIP_API_PASSWORD" && exit 1)
	@test -n "$(SHIP_CUSTOMER_ID)" || (echo "Missing SHIP_CUSTOMER_ID" && exit 1)
	@test -n "$(SHIP_CONSIGNEE_CITY)" || (echo "Missing SHIP_CONSIGNEE_CITY" && exit 1)
	@test -n "$(SHIP_CONSIGNEE_STREET)" || (echo "Missing SHIP_CONSIGNEE_STREET" && exit 1)
	@test -n "$(SHIP_CONSIGNEE_HOUSE_NUMBER)" || (echo "Missing SHIP_CONSIGNEE_HOUSE_NUMBER" && exit 1)
	@test -n "$(SHIP_CONSIGNEE_CONTACT_PERSON)" || (echo "Missing SHIP_CONSIGNEE_CONTACT_PERSON" && exit 1)
	@test -n "$(SHIP_CONSIGNEE_CUSTOMER_NAME)" || (echo "Missing SHIP_CONSIGNEE_CUSTOMER_NAME" && exit 1)
	@test -n "$(SHIP_CONSIGNEE_PHONE)" || (echo "Missing SHIP_CONSIGNEE_PHONE" && exit 1)
	@test -n "$(SHIP_PICKUP_POINT_TYPE)" || (echo "Missing SHIP_PICKUP_POINT_TYPE" && exit 1)
	@test -n "$(SHIP_PICKUP_POINT_ID)" || (echo "Missing SHIP_PICKUP_POINT_ID" && exit 1)
	@echo "🚀 Running insert-pickup-shipment example..."
	PYTHONPATH=src SHIP_API_USER="$(SHIP_API_USER)" SHIP_API_PASSWORD="$(SHIP_API_PASSWORD)" SHIP_CUSTOMER_ID="$(SHIP_CUSTOMER_ID)" SHIP_ENV="$(or $(SHIP_ENV),DEV)" SHIP_CONSIGNEE_CITY="$(SHIP_CONSIGNEE_CITY)" SHIP_CONSIGNEE_STREET="$(SHIP_CONSIGNEE_STREET)" SHIP_CONSIGNEE_HOUSE_NUMBER="$(SHIP_CONSIGNEE_HOUSE_NUMBER)" SHIP_CONSIGNEE_CONTACT_PERSON="$(SHIP_CONSIGNEE_CONTACT_PERSON)" SHIP_CONSIGNEE_CUSTOMER_NAME="$(SHIP_CONSIGNEE_CUSTOMER_NAME)" SHIP_CONSIGNEE_PHONE="$(SHIP_CONSIGNEE_PHONE)" SHIP_PICKUP_POINT_TYPE="$(SHIP_PICKUP_POINT_TYPE)" SHIP_PICKUP_POINT_ID="$(SHIP_PICKUP_POINT_ID)" SHIP_REFERENCE_1="$(SHIP_REFERENCE_1)" SHIP_REFERENCE_2="$(SHIP_REFERENCE_2)" SHIP_SHIPMENT_INSTRUCTIONS="$(SHIP_SHIPMENT_INSTRUCTIONS)" SHIP_USE_DEFAULT_SHIPPER_ADDRESS="$(or $(SHIP_USE_DEFAULT_SHIPPER_ADDRESS),true)" SHIP_NUMBER_OF_PACKAGES="$(or $(SHIP_NUMBER_OF_PACKAGES),1)" SHIP_CONTEXT_USER_EMAIL="$(SHIP_CONTEXT_USER_EMAIL)" SHIP_USER_DISPLAY_NAME="$(SHIP_USER_DISPLAY_NAME)" SHIP_ORIGINAL_DATA="$(SHIP_ORIGINAL_DATA)" $(VENV_BIN)/python examples/insertpickupshipmentex.py

example-get-wb-thermal-or-a4-for-print:
	@test -n "$(SHIP_API_USER)" || (echo "Missing SHIP_API_USER" && exit 1)
	@test -n "$(SHIP_API_PASSWORD)" || (echo "Missing SHIP_API_PASSWORD" && exit 1)
	@test -n "$(SHIP_CUSTOMER_ID)" || (echo "Missing SHIP_CUSTOMER_ID" && exit 1)
	@test -n "$(SHIP_TRACKING_NUMBER)" || (echo "Missing SHIP_TRACKING_NUMBER" && exit 1)
	@echo "🚀 Running label-download example..."
	PYTHONPATH=src SHIP_API_USER="$(SHIP_API_USER)" SHIP_API_PASSWORD="$(SHIP_API_PASSWORD)" SHIP_CUSTOMER_ID="$(SHIP_CUSTOMER_ID)" SHIP_ENV="$(or $(SHIP_ENV),DEV)" SHIP_TRACKING_NUMBER="$(SHIP_TRACKING_NUMBER)" SHIP_LABEL_FORMAT="$(or $(SHIP_LABEL_FORMAT),thermal)" SHIP_LABEL_COPIES="$(or $(SHIP_LABEL_COPIES),3)" SHIP_LABEL_OUTPUT="$(SHIP_LABEL_OUTPUT)" $(VENV_BIN)/python examples/get-wb-thermal-or-a4-for-print.py
