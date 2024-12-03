CREATE TABLE "occupations" (
  "occupation_id" INT PRIMARY KEY,
  "attribute_id" INT,
  "person_id" INT,
  "work" VARCHAR(45)
);

CREATE TABLE "marital_levels" (
  "marital_level_id" INT PRIMARY KEY,
  "attribute_id" INT,
  "person_id" INT,
  "marital_status" VARCHAR(45)
);

CREATE TABLE "property_ownership" (
  "ownership_id" INT PRIMARY KEY,
  "attribute_id" INT,
  "person_id" INT,
  "owned_rented" VARCHAR(45)
);

CREATE TABLE "personal_attributes" (
  "attribute_id" INT PRIMARY KEY,
  "person_id" INT,
  "race" VARCHAR(45),
  "sex" VARCHAR(45),
  "age" INT
);

CREATE TABLE "persons" (
  "person_id" INT PRIMARY KEY,
  "first_name" VARCHAR(45),
  "last_name" VARCHAR(45),
  "personal_attribute_id" INT,
  "family_id" INT,
  "relationship_id" INT,
  "marital_level_id" INT,
  "property_ownership_id" INT,
  "occupation_id" INT
);

CREATE TABLE "relationships" (
  "relationship_id" INT PRIMARY KEY,
  "attribute_id" INT,
  "person_id" INT,
  "family_id" INT,
  "relation_to_hoh" VARCHAR(45)
);

CREATE TABLE "families" (
  "family_id" INT PRIMARY KEY,
  "person_id" INT,
  "family" INT,
  "dwelling" INT,
  "hoh_first_name" VARCHAR(45),
  "hoh_last_name" VARCHAR(45),
  "relationship_id" INT
);

ALTER TABLE "persons" ADD FOREIGN KEY ("personal_attribute_id") REFERENCES "personal_attributes" ("attribute_id");

ALTER TABLE "persons" ADD FOREIGN KEY ("family_id") REFERENCES "families" ("family_id");

ALTER TABLE "persons" ADD FOREIGN KEY ("relationship_id") REFERENCES "relationships" ("relationship_id");

ALTER TABLE "persons" ADD FOREIGN KEY ("marital_level_id") REFERENCES "marital_levels" ("marital_level_id");

ALTER TABLE "persons" ADD FOREIGN KEY ("property_ownership_id") REFERENCES "property_ownership" ("ownership_id");

ALTER TABLE "persons" ADD FOREIGN KEY ("occupation_id") REFERENCES "occupations" ("occupation_id");

ALTER TABLE "families" ADD FOREIGN KEY ("relationship_id") REFERENCES "relationships" ("relationship_id");
