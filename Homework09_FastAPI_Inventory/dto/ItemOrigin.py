from pydantic import BaseModel, field_validator


class ItemOrigin(BaseModel):
    country: str
    production_date: str

    @field_validator("country") #try to define custome valid data for the field_country
    @classmethod #you only make sub-sequent function available to the class, not the object
    def check_valid_country(cls, country: str): #defind class method
        assert country == "Ethiopia", "Country's name must be Ethiopia"
        return(country)