"""
APIForge: Enhanced API route generation with proper model handling.
Integrates with ModelForge for model management and route generation.
"""
from typing import Dict, List, Optional
from enum import Enum
# import session
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, Field, ConfigDict
from sqlalchemy import text
from pydantic.main import create_model

from forge.utils import *
from forge.model import ModelForge
from forge.gen.crud import CRUD
# from forge.gen.view import register_view_routes

class RouteType(str, Enum):
    """Available route types."""
    CREATE = "create"
    READ = "read"
    UPDATE = "update"
    DELETE = "delete"

class APIForge(BaseModel):
    """
    Manages API route generation and CRUD operations.
    Works in conjunction with ModelForge for model handling.
    """
    model_forge: ModelForge  # * ModelForge instance for model management
    routers: Dict[str, APIRouter] = Field(default_factory=dict)

    model_config = ConfigDict(arbitrary_types_allowed=True)

    def __init__(self, **data):
        super().__init__(**data)
        # * Initialize the routers for each schema
        for schema in sorted(self.model_forge.include_schemas):
            self.routers[schema] = APIRouter(prefix=f"/{schema}", tags=[schema.upper()])
            # self.routers[f"{schema}_views"] = APIRouter(prefix=f"/{schema}/views", tags=[f"{schema.upper()} Views"])

    def gen_table_routes(self) -> None:
        """Generate CRUD routes for all tables in the model cache."""
        print(f"\n{bold('[Generating Routes]')}")
        [self.gen_table_crud(*table.split(".")) for table in self.model_forge.model_cache.keys()]

    def gen_table_crud(self, schema: str,  table_name: str) -> None:
        """Generate the curd routes for a certain Table..."""
        full_table_name = f"{schema}.{table_name}"
        if full_table_name not in self.model_forge.model_cache:
            raise KeyError(f"No models found for {full_table_name}")

        pydantic_model, sqlalchemy_model = self.model_forge.model_cache[full_table_name]
        CRUD(
            table=self.model_forge.db_manager.metadata.tables[full_table_name],
            pydantic_model=pydantic_model,
            sqlalchemy_model=sqlalchemy_model,
            router=self.routers[schema],
            db_dependency=self.model_forge.db_manager.get_db,
            tags=[schema.upper()]
        ).generate_all()

        print(f"\t{gray('gen crud for:')} {cyan(full_table_name)}")

    # todo: Improve the way the view routes are generated...
    def gen_view_routes(self) -> None:
        """Generate CRUD routes for all views in the view cache."""
        print(f"\n{bold('[Generating View Routes]')}")
        [self.gen_view_route(view) for view in self.model_forge.view_cache.keys()]

    def gen_view_route(self, view_name: str) -> None:
        """Generates the GET route for a View with automatic model generation."""
        if view_name not in self.model_forge.view_cache:
            raise KeyError(f"No views found for {view_name}")

        # Get the actual Table object from metadata
        view_table = self.model_forge.view_cache[view_name]
        schema = view_table.schema

        print(f"\t{gray('gen view for:')} {cyan(view_name)}")

        # Create query params model for filtering
        view_query_fields = {}
        for column in view_table.columns:
            field_type = get_eq_type(str(column.type))
            # Make all fields optional for query params
            view_query_fields[column.name] = (Optional[field_type], Field(default=None))

        # todo: Move this stuff to the ModelForge
        # todo: - because the ModelForge should be the one handling the model generation

        ViewQueryParams = create_model(
            f"View_{view_table.name}_QueryParams",
            **view_query_fields,
            __base__=BaseModel
        )
        
        # Create the main Pydantic model for response
        ViewPydanticModel = create_model(
            f"View_{view_table.name}",
            __config__=ConfigDict(
                from_attributes=True,
                populate_by_name=True,
                arbitrary_types_allowed=True,
            ),
            **{name: (type_, Field(default=None)) for name, (type_, _) in view_query_fields.items()}
        )

        @self.routers[f"{schema}"].get(
            f"/{view_table.name}",
            response_model=List[ViewPydanticModel],
            tags=[f"{schema.upper()} Views"],
            summary=f"Get {view_table.name} view data",
            description=(
                f"Retrieve records from the {view_table.name} view with optional filtering, "
                "ordering, and pagination"
            )
        )
        def get_view_data(
            db: Session = Depends(self.model_forge.db_manager.get_db),
            filters: ViewQueryParams = Depends(),
            # limit: Optional[int] = Query(50, ge=1, description="Number of records to return"),
            # offset: Optional[int] = Query(0, ge=0, description="Number of records to skip"),
            # order_by: Optional[str] = Query(None, description="Column to order by"),
            # order_dir: Optional[str] = Query(
            #     "asc", 
            #     enum=["asc", "desc"], 
            #     description="Sort direction"
            # ),
        ) -> List[ViewPydanticModel]:
            # Start building the SQL query
            query_parts = [f'SELECT * FROM {schema}.{view_table.name}']
            params = {}

            # Add WHERE clauses for filters
            filter_conditions = []
            for field_name, value in filters.model_dump(exclude_unset=True).items():
                if value is not None:
                    param_name = f"param_{field_name}"
                    filter_conditions.append(f"{field_name} = :{param_name}")
                    params[param_name] = value

            if filter_conditions:
                query_parts.append("WHERE " + " AND ".join(filter_conditions))

            # # Add ORDER BY if specified
            # if order_by and order_by in [col.name for col in view_table.columns]:
            #     query_parts.append(f"ORDER BY {order_by} {order_dir.upper()}")

            # # Add LIMIT and OFFSET
            # if limit is not None:
            #     query_parts.append(f"LIMIT :limit")
            #     params["limit"] = limit
            
            # if offset is not None:
            #     query_parts.append(f"OFFSET :offset")
            #     params["offset"] = offset

            records = [dict(row._mapping) for row in db.execute(text(" ".join(query_parts)), params)]
            return [ViewPydanticModel.model_validate(record) for record in records]
