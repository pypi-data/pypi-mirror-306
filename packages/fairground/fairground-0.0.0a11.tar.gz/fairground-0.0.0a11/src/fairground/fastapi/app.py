"""The FastAPI app."""

import datetime as dt
import sys

import pandas as pd
import uvicorn
from fastapi import APIRouter, FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from presidio_anonymizer.entities import OperatorConfig
from presidio_structured import PandasAnalysisBuilder, StructuredEngine
from pydantic import BaseModel, ConfigDict, TypeAdapter
from pydantic.alias_generators import to_camel

from .. import intersectional


class Person(BaseModel):
    """Represents a Person."""

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    first_name: str
    last_name: str
    dob: str
    visits: int
    status: str
    progress: int


# Mock data - replace with your actual data source
mock_data = [
    Person(
        first_name="John",
        last_name="Doe",
        dob=dt.date(1980, 1, 1).strftime("%Y-%m-%d"),
        visits=10,
        status="Active",
        progress=50,
    ),
    Person(
        first_name="Jane",
        last_name="Smith",
        dob=dt.date(1985, 2, 15).strftime("%Y-%m-%d"),
        visits=5,
        status="Inactive",
        progress=80,
    ),
    Person(
        first_name="Bob",
        last_name="Johnson",
        dob=dt.date(1970, 3, 20).strftime("%Y-%m-%d"),
        visits=20,
        status="Active",
        progress=75,
    ),
    Person(
        first_name="Alice",
        last_name="Williams",
        dob=dt.date(1982, 4, 25).strftime("%Y-%m-%d"),
        visits=15,
        status="Active",
        progress=60,
    ),
    Person(
        first_name="Charlie",
        last_name="Brown",
        dob=dt.date(1988, 5, 30).strftime("%Y-%m-%d"),
        visits=8,
        status="Inactive",
        progress=40,
    ),
    Person(
        first_name="Eva",
        last_name="Davis",
        dob=dt.date(1988, 5, 30).strftime("%Y-%m-%d"),
        visits=12,
        status="Active",
        progress=90,
    ),
    Person(
        first_name="Frank",
        last_name="Miller",
        dob=dt.date(1988, 5, 30).strftime("%Y-%m-%d"),
        visits=25,
        status="Active",
        progress=85,
    ),
]

router = APIRouter()


@router.get("/data", response_model=list[Person])
async def get_data() -> list[Person]:
    """Return the raw mock data without modification."""
    return mock_data


@router.post("/process", response_model=list[Person])
async def process_data(data: list[Person]) -> list[Person]:
    """Process a list of Person objects and return them anonymized."""
    # Convert input data to a DataFrame
    sensitive_df = pd.DataFrame([p.model_dump() for p in data])

    # Initialize the Presidio Structured engine
    pandas_engine = StructuredEngine()

    # Generate a tabular analysis
    tabular_analysis = PandasAnalysisBuilder().generate_analysis(sensitive_df)

    operators = {
        "PERSON": OperatorConfig("replace", {"new_value": "<ANONYMIZED PERSON>"}),
        "DATE_TIME": OperatorConfig("replace", {"new_value": "<ANONYMIZED DATE OF BIRTH>"}),
        "STATUS": OperatorConfig("replace", {"new_value": "<ANONYMIZED>"}),
        # Add more operators for other entity types if needed
    }

    # Anonymize DataFrame
    anonymized_df = pandas_engine.anonymize(sensitive_df, tabular_analysis, operators=operators)
    assert isinstance(anonymized_df, pd.DataFrame)

    # Convert DataFrame back to list of Person objects
    return TypeAdapter(list[Person]).validate_python(anonymized_df.to_dict("records"))


class AnalysisResult(BaseModel):
    """An Analysis Result."""

    result: str


@router.post("/analyse_as_univariate")
def analyse_univariate(file: UploadFile) -> AnalysisResult:
    """Univariate Analysis."""
    uni_df = pd.read_csv(file.file)
    result = intersectional.univariate(uni_df)
    return AnalysisResult(result=result)


@router.post("/analyse_as_bivariate")
def analyse_bivariate(file: UploadFile) -> AnalysisResult:
    """Bivariate Analysis."""
    bi_df = pd.read_csv(file.file)
    result = intersectional.univariate(bi_df)
    return AnalysisResult(result=result)


@router.post("/analyse_as_multivariate")
def analyse_multivariate(file: UploadFile) -> AnalysisResult:
    """Multivariate Analysis."""
    multi_df = pd.read_csv(file.file)
    result = intersectional.univariate(multi_df)
    return AnalysisResult(result=result)


def create_app() -> FastAPI:
    """App factory."""
    app = FastAPI()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Adjust this to your React app's URL
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(router)

    return app


def main() -> int:
    """Run the dev server."""
    uvicorn.run(f"{__spec__.name}:create_app", host="localhost", port=8000, factory=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
