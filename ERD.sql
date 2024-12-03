CREATE TABLE "census_records" (
  "record_id" int PRIMARY KEY,
  "census_year" int,
  "person_id" int,
  "source_pk" int
);

CREATE TABLE "occupations" (
  "occupation_id" int PRIMARY KEY,
  "attribute_id" int,
  "person_id" int,
  "work" varchar(45),
  "business" varchar(45),
  "record_id" int
);

CREATE TABLE "marital_levels" (
  "marital_level_id" int PRIMARY KEY,
  "attribute_id" int,
  "person_id" int,
  "marital_status" varchar(45),
  "record_id" int
);

CREATE TABLE "property_ownership" (
  "ownership_id" int PRIMARY KEY,
  "attribute_id" int,
  "person_id" int,
  "owned_rented" varchar(45),
  "record_id" int
);

CREATE TABLE "personal_attributes" (
  "attribute_id" int PRIMARY KEY,
  "person_id" int,
  "race" varchar(45),
  "sex" varchar(45),
  "age" int,
  "record_id" int
);

CREATE TABLE "persons" (
  "person_id" int PRIMARY KEY,
  "first_name" varchar(45),
  "last_name" varchar(45),
  "personal_attribute_id" int,
  "family_id" int,
  "relationship_id" int,
  "marital_level_id" int,
  "property_ownership_id" int,
  "occupation_id" int
);

CREATE TABLE "relationships" (
  "relationship_id" int PRIMARY KEY,
  "attribute_id" int,
  "person_id" int,
  "family_id" int,
  "relation_to_hoh" varchar(45),
  "record_id" int
);

CREATE TABLE "families" (
  "family_id" int PRIMARY KEY,
  "person_id" int,
  "family" int,
  "dwelling" int,
  "hoh_first_name" varchar(45),
  "hoh_last_name" varchar(45),
  "relationship_id" int,
  "census_year" int
);

CREATE INDEX ON "census_records" ("census_year");

CREATE INDEX ON "census_records" ("person_id");

CREATE INDEX ON "occupations" ("person_id");

CREATE INDEX ON "occupations" ("record_id");

CREATE INDEX ON "marital_levels" ("person_id");

CREATE INDEX ON "marital_levels" ("record_id");

CREATE INDEX ON "property_ownership" ("person_id");

CREATE INDEX ON "property_ownership" ("record_id");

CREATE INDEX ON "personal_attributes" ("person_id");

CREATE INDEX ON "personal_attributes" ("record_id");

CREATE INDEX ON "persons" ("last_name", "first_name");

CREATE INDEX ON "relationships" ("person_id");

CREATE INDEX ON "relationships" ("family_id");

CREATE INDEX ON "relationships" ("record_id");

CREATE INDEX ON "families" ("census_year");

CREATE INDEX ON "families" ("hoh_last_name", "hoh_first_name");

ALTER TABLE "persons" ADD FOREIGN KEY ("personal_attribute_id") REFERENCES "personal_attributes" ("attribute_id");

ALTER TABLE "persons" ADD FOREIGN KEY ("family_id") REFERENCES "families" ("family_id");

ALTER TABLE "persons" ADD FOREIGN KEY ("relationship_id") REFERENCES "relationships" ("relationship_id");

ALTER TABLE "persons" ADD FOREIGN KEY ("marital_level_id") REFERENCES "marital_levels" ("marital_level_id");

ALTER TABLE "persons" ADD FOREIGN KEY ("property_ownership_id") REFERENCES "property_ownership" ("ownership_id");

ALTER TABLE "persons" ADD FOREIGN KEY ("occupation_id") REFERENCES "occupations" ("occupation_id");

ALTER TABLE "families" ADD FOREIGN KEY ("relationship_id") REFERENCES "relationships" ("relationship_id");

ALTER TABLE "occupations" ADD FOREIGN KEY ("record_id") REFERENCES "census_records" ("record_id");

ALTER TABLE "marital_levels" ADD FOREIGN KEY ("record_id") REFERENCES "census_records" ("record_id");

ALTER TABLE "property_ownership" ADD FOREIGN KEY ("record_id") REFERENCES "census_records" ("record_id");

ALTER TABLE "personal_attributes" ADD FOREIGN KEY ("record_id") REFERENCES "census_records" ("record_id");

ALTER TABLE "relationships" ADD FOREIGN KEY ("record_id") REFERENCES "census_records" ("record_id");

ALTER TABLE "census_records" ADD FOREIGN KEY ("person_id") REFERENCES "persons" ("person_id");
