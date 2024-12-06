CREATE TABLE "census_records" (
  "record_id" INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
  "census_year" int NOT NULL,
  "source_pk" int NOT NULL,
  "ed" varchar(50),
  "page_number" varchar(50),
  "created_at" timestamp DEFAULT (CURRENT_TIMESTAMP)
);

CREATE TABLE "locations" (
  "location_id" INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
  "record_id" int NOT NULL,
  "street_name" varchar(100),
  "house_num" varchar(50),
  "build_num" varchar(50),
  "dwelling_number" varchar(50),
  "family_number" varchar(50),
  "created_at" timestamp DEFAULT (CURRENT_TIMESTAMP)
);

CREATE TABLE "persons" (
  "person_id" varchar(50) PRIMARY KEY,
  "first_name" varchar(100) NOT NULL,
  "last_name" varchar(100) NOT NULL,
  "created_at" timestamp DEFAULT (CURRENT_TIMESTAMP)
);

CREATE TABLE "personal_attributes" (
  "attribute_id" INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
  "person_id" varchar(50) NOT NULL,
  "record_id" int NOT NULL,
  "sex" varchar(45),
  "race" varchar(45),
  "age" int,
  "place_birth" varchar(100),
  "created_at" timestamp DEFAULT (CURRENT_TIMESTAMP)
);

CREATE TABLE "occupations" (
  "occupation_id" INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
  "person_id" varchar(50) NOT NULL,
  "record_id" int NOT NULL,
  "work" varchar(100),
  "business" varchar(100),
  "created_at" timestamp DEFAULT (CURRENT_TIMESTAMP)
);

CREATE TABLE "families" (
  "family_id" varchar(50) PRIMARY KEY,
  "record_id" int NOT NULL,
  "location_id" int NOT NULL,
  "head_first_name" varchar(100),
  "head_last_name" varchar(100),
  "created_at" timestamp DEFAULT (CURRENT_TIMESTAMP)
);

CREATE TABLE "relationships" (
  "relationship_id" INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
  "person_id" varchar(50) NOT NULL,
  "family_id" varchar(50) NOT NULL,
  "record_id" int NOT NULL,
  "relation_to_head" varchar(100),
  "created_at" timestamp DEFAULT (CURRENT_TIMESTAMP)
);

CREATE TABLE "property_status" (
  "property_id" INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
  "person_id" varchar(50) NOT NULL,
  "record_id" int NOT NULL,
  "owned_rented" varchar(45),
  "created_at" timestamp DEFAULT (CURRENT_TIMESTAMP)
);

CREATE TABLE "marital_status" (
  "marital_id" INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
  "person_id" varchar(50) NOT NULL,
  "record_id" int NOT NULL,
  "marital_status" varchar(45),
  "created_at" timestamp DEFAULT (CURRENT_TIMESTAMP)
);

ALTER TABLE "personal_attributes" ADD FOREIGN KEY ("person_id") REFERENCES "persons" ("person_id");

ALTER TABLE "personal_attributes" ADD FOREIGN KEY ("record_id") REFERENCES "census_records" ("record_id");

ALTER TABLE "occupations" ADD FOREIGN KEY ("person_id") REFERENCES "persons" ("person_id");

ALTER TABLE "occupations" ADD FOREIGN KEY ("record_id") REFERENCES "census_records" ("record_id");

ALTER TABLE "locations" ADD FOREIGN KEY ("record_id") REFERENCES "census_records" ("record_id");

ALTER TABLE "families" ADD FOREIGN KEY ("record_id") REFERENCES "census_records" ("record_id");

ALTER TABLE "families" ADD FOREIGN KEY ("location_id") REFERENCES "locations" ("location_id");

ALTER TABLE "relationships" ADD FOREIGN KEY ("person_id") REFERENCES "persons" ("person_id");

ALTER TABLE "relationships" ADD FOREIGN KEY ("family_id") REFERENCES "families" ("family_id");

ALTER TABLE "relationships" ADD FOREIGN KEY ("record_id") REFERENCES "census_records" ("record_id");

ALTER TABLE "property_status" ADD FOREIGN KEY ("person_id") REFERENCES "persons" ("person_id");

ALTER TABLE "property_status" ADD FOREIGN KEY ("record_id") REFERENCES "census_records" ("record_id");

ALTER TABLE "marital_status" ADD FOREIGN KEY ("person_id") REFERENCES "persons" ("person_id");

ALTER TABLE "marital_status" ADD FOREIGN KEY ("record_id") REFERENCES "census_records" ("record_id");