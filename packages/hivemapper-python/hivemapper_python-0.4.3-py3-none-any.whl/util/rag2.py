import csv
from json import loads
from dotenv import load_dotenv
from tqdm import tqdm
from graphrag_sdk.orchestrator import Orchestrator
from graphrag_sdk.agents.kg_agent import KGAgent
from graphrag_sdk.models.openai import OpenAiGenerativeModel
from graphrag_sdk import (
    Ontology, Entity, Relation, Attribute, AttributeType, KnowledgeGraph, KnowledgeGraphModelConfig
)

# Load environment variables
load_dotenv()

# Almanac Ontology
almanac_ontology = Ontology()

# Manually created Ontology by adding entities and relations
almanac_ontology.add_entity(
    Entity(
        label="Region",
        attributes=[
            Attribute(
                name="oid",
                attr_type=AttributeType.STRING,
                required=True,
                unique=True,
            ),
            Attribute(
                name="name",
                attr_type=AttributeType.STRING,
                required=True,
                unique=True,
            ),
            Attribute(
                name="shortName",
                attr_type=AttributeType.STRING,
                required=False,
                unique=False,
            ),
            Attribute(
                name="description",
                attr_type=AttributeType.STRING,
                required=False,
                unique=False,
            ),
        ],
        description="A Region is usually a city or metro area that contains roads, intersetions, places, speed limit signs, stop signs, traffic lights, and turn restriction signs."
    )
)

almanac_ontology.add_entity(
    Entity(
        label="Intersection",
        attributes=[
            Attribute(
                name="oid",
                attr_type=AttributeType.STRING,
                required=True,
                unique=True,
            ),
            Attribute(
                name="loc",
                attr_type=AttributeType.POINT,
                required=True,
                unique=False,
            ),
        ],
        description="Intersections are connected by Roads. Intersections can have places, stop signs, turn restrictions, and traffic lights."
    )
)

almanac_ontology.add_entity(
    Entity(
        label="Place",
        attributes=[
            Attribute(
                name="oid",
                attr_type=AttributeType.STRING,
                required=True,
                unique=True,
            ),
            Attribute(
                name="name",
                attr_type=AttributeType.STRING,
                required=False,
                unique=False,
            ),
            Attribute(
                name="category",
                attr_type=AttributeType.STRING,
                required=False,
                unique=False,
            ),
            Attribute(
                name="address",
                attr_type=AttributeType.STRING,
                required=False,
                unique=False,
            ),
            Attribute(
                name="loc",
                attr_type=AttributeType.POINT,
                required=True,
                unique=False,
            ),
        ],
        description="A Place has a category and a name and are connected by roads.  Places can be schools."
    )
)

almanac_ontology.add_entity(
    Entity(
        label="TurnRestriction",
        attributes=[
            Attribute(
                name="oid",
                attr_type=AttributeType.STRING,
                required=True,
                unique=True,
            ),
            Attribute(
                name="rule",
                attr_type=AttributeType.STRING,
                required=True,
                unique=False,
            ),
            Attribute(
                name="loc",
                attr_type=AttributeType.POINT,
                required=True,
                unique=False,
            ),
            Attribute(
                name="azimuth",
                attr_type=AttributeType.NUMBER,
                required=True,
                unique=False,
            ),
            Attribute(
                name="on_red",
                attr_type=AttributeType.BOOLEAN,
                required=True,
                unique=False,
            ),
            Attribute(
                name="turn_restriction",
                attr_type=AttributeType.STRING,
                required=False,
                unique=False,
            ),
        ],
        description="A turn restriction.",
    )
)


almanac_ontology.add_entity(
    Entity(
        label="StopSign",
        attributes=[
            Attribute(
                name="oid",
                attr_type=AttributeType.STRING,
                required=True,
                unique=True,
            ),
            Attribute(
                name="loc",
                attr_type=AttributeType.POINT,
                required=True,
                unique=False,
            ),
            Attribute(
                name="azimuth",
                attr_type=AttributeType.NUMBER,
                required=True,
                unique=False,
            ),
        ],
        description="A stop sign.",
    )
)


almanac_ontology.add_entity(
    Entity(
        label="TrafficLight",
        attributes=[
            Attribute(
                name="oid",
                attr_type=AttributeType.STRING,
                required=True,
                unique=True,
            ),
            Attribute(
                name="loc",
                attr_type=AttributeType.POINT,
                required=True,
                unique=False,
            ),
            Attribute(
                name="azimuth",
                attr_type=AttributeType.NUMBER,
                required=True,
                unique=False,
            ),
        ],
        description="A traffic light.",
    )
)

almanac_ontology.add_relation(
    Relation(
        label="HAS_INTERSECTION",
        source="Region",
        target="Intersection",
    )
)
almanac_ontology.add_relation(
    Relation(
        label="HAS_PLACE",
        source="Region",
        target="Place",
    )
)
almanac_ontology.add_relation(
    Relation(
        label="ROAD",
        source="Intersection",
        target="Intersection",
        attributes=[
            Attribute(
                name="oid",
                attr_type=AttributeType.STRING,
                required=True,
                unique=True,
            ),
            Attribute(
                name="name",
                attr_type=AttributeType.STRING,
                required=False,
                unique=False,
            ),
            Attribute(
                name="loc",
                attr_type=AttributeType.POINT,
                required=True,
                unique=False,
            ),
            Attribute(
                name="speedLimit",
                attr_type=AttributeType.NUMBER,
                required=False,
                unique=False,
            ),
            Attribute(
                name="schoolZone",
                attr_type=AttributeType.BOOLEAN,
                required=True,
                unique=False,
            ),
            Attribute(
                name="regulatorySpeedLimitMF",
                attr_type=AttributeType.STRING,
                required=False,
                unique=False,
            ),
            Attribute(
                name="class",
                attr_type=AttributeType.STRING,
                required=True,
                unique=False,
            ),
            Attribute(
                name="length",
                attr_type=AttributeType.NUMBER,
                required=True,
                unique=False,
            ),
        ],
        description='A road segment that connects two intersections.'
    )
)
almanac_ontology.add_relation(
    Relation(
        label="IS_NEAR_PLACE",
        source="Intersection",
        target="Place",
    )
)
almanac_ontology.add_relation(
    Relation(
        label="NEAREST_INTERSECTION",
        source="Place",
        target="Intersection",
    )
)
almanac_ontology.add_relation(
    Relation(
        label="HAS_STOPSIGN",
        source="Intersection",
        target="StopSign",
    )
)
almanac_ontology.add_relation(
    Relation(
        label="HAS_TURNRESTRICTION",
        source="Intersection",
        target="TurnRestriction",
    )
)
almanac_ontology.add_relation(
    Relation(
        label="HAS_TRAFFICLIGHT",
        source="Intersection",
        target="TrafficLight",
    )
)

# Define the model
model = OpenAiGenerativeModel("gpt-4o")

# Create the KG from the predefined ontology.
almanac_kg = KnowledgeGraph(
    name="almanac",
    ontology=almanac_ontology,
    model_config=KnowledgeGraphModelConfig.with_model(model),
    host='35.89.101.3'
)
