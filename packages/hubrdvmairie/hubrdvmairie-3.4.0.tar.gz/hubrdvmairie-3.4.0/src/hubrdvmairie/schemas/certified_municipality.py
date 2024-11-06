from pydantic import BaseModel, Field


class CertifiedMunicipalityBase(BaseModel):
    """
    Certified Municipality  schema.
    """

    ugf: str = Field(..., max_length=5)
    town_hall_name: str = Field(..., max_length=255)
    address: str
    zip_code: str = Field(..., max_length=5)
    city_name: str = Field(..., max_length=100)
    phone_number: str
    website: str = Field(..., max_length=255)
    appointment_details: str
    service_opening_date: str
    label: str = Field(..., max_length=255)

    def __hash__(self):
        return hash(
            (
                self.ugf,
                self.town_hall_name,
                self.address,
                self.zip_code,
                self.city_name,
                self.phone_number,
                self.website,
                self.appointment_details,
                self.service_opening_date,
                self.label,
            )
        )


class CertifiedMunicipalityCreate(CertifiedMunicipalityBase):
    """
    Certified Municipality create schema.
    """


class CertifiedMunicipalityUpdate(CertifiedMunicipalityBase):
    """
    Certified Municipality update schema.
    """


class CertifiedMunicipality(CertifiedMunicipalityBase):
    """
    Certified Municipality schema.
    """

    class Config:
        orm_mode = True
