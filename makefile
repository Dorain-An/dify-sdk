define PRINT_HELP_PYSCRIPT
import re, sys

print("make option")
print("  --option:")
for line in sys.stdin:
    match = re.match(r'^([0-9a-zA-Z_-]+):.*?## (.*)$$', line)
    if match:
        target, help = match.groups()
        print("    {:<20}{}".format(target, help))
endef
export PRINT_HELP_PYSCRIPT

NJOBS := $(shell expr `python -c "from multiprocessing import cpu_count; print(cpu_count())"` - 1)
BROWSER := python -c "$$BROWSER_PYSCRIPT"
SOURCES := src

help: ## 帮助信息
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

lint-mypy: ## 类型注解检查
	mypy ${SOURCES}

lint-black: ## 格式化检查
	black ${SOURCES} --check

lint-isort: ## import排序检查
	isort --check-only ${SOURCES}

lint-flake8: ## flake8检查
	flake8 ${SOURCES} --jobs=$(NJOBS)

lint-pylint: ## pylint检查
	pylint ${SOURCES} --jobs=$(NJOBS)

lint-bandit: ## 代码风险检查
	bandit -c pyproject.toml -r ${SOURCES}

lint: lint-mypy lint-black lint-isort lint-flake8 lint-pylint lint-bandit ## 检查代码

format: ## 代码格式化
	autoflake --remove-all-unused-imports --recursive --remove-unused-variables --in-place ${SOURCES} --exclude=__init__.py,api2.py
	isort ${SOURCES}
	black ${SOURCES}

clean-pyc: ## 清理 Python 运行文件
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '*.log' -exec rm -f {} +
	find . -name '*.log.*' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -rf {} +
	find . -name '.mypy_cache' -exec rm -rf {} +
	find . -name '*.egg-info' -exec rm -rf {} +
	find . -name '.DS_Store' -exec rm -rf {} +
	find . -name 'redbeat.RedBeatScheduler' -exec rm -rf {} +
	find . -name 'celerybeat-schedule' -exec rm -rf {} +
	find . -name 'celerybeat.pid' -exec rm -rf {} +

clean: clean-pyc  ## 清理所有不该进代码库的文件

gen-deps: ## 生成依赖文件
	pip-compile --resolver=backtracking requirements.in -o requirements.txt
	pip-compile --resolver=backtracking requirements-dev.in -o requirements-dev.txt

upgrade-deps: ## 依赖文件升级
	pip-compile --resolver=backtracking requirements.in -o requirements.txt --upgrade
	pip-compile --resolver=backtracking requirements-dev.in -o requirements-dev.txt --upgrade
