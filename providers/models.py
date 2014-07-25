from django.db import models

# Create your models here.
class Provider(models.Model):
    npi = models.PositiveIntegerField()
    replacement_npi = models.PositiveIntegerField()
    entity_type_code = models.PositiveSmallIntegerField()

    def __unicode__(self):
        return str(self.npi)
# end Provider

class Taxonomy(models.Model):
    npi = models.PositiveIntegerField()
    taxonomy_code = models.CharField(max_length=20)
    license_number = models.CharField(max_length=20)
    state_code = models.CharField(max_length=2)
    primary_taxonomy_switch = models.CharField(max_length=1)

    def __unicode__(self):
        return u'%s - %s' % (self.npi, self.taxonomy_code)
# end Taxonomy

class OtherProvider(models.Model):
    npi = models.PositiveIntegerField()
    identifier = models.CharField(max_length=20)
    type_code = models.CharField(max_length=2)
    state = models.CharField(max_length=2)
    issuer = models.CharField(max_length=80)
# end OtherProvider

class TaxonomyGroup(models.Model):
    npi = models.PositiveIntegerField()
    taxonomy_group = models.CharField(max_length=70)
# end TaxonomyGroup

class PracticeAddress(models.Model):
    address_first_line = models.CharField(max_length=55)
    address_second_line = models.CharField(max_length=55)
    city_name = models.CharField(max_length=40)
    state_name = models.CharField(max_length=40)
    postal_code = models.CharField(max_length=20)
    country_code = models.CharField(max_length=2)
# end PracticeAddress

class MailingAddress(models.Model):
    address_first_line = models.CharField(max_length=55)
    address_second_line = models.CharField(max_length=55)
    city_name = models.CharField(max_length=40)
    state_name = models.CharField(max_length=40)
    postal_code = models.CharField(max_length=20)
    country_code = models.CharField(max_length=2)
# end MailingAddress

class Organization(models.Model):
    employer_identification_number = models.CharField(max_length=9)
    organization_name = models.CharField(max_length=70)
    other_name = models.CharField(max_length=70)
    type_code = models.CharField(max_length=1)
    is_organization_subpart = models.CharField(max_length=1)
# end Organization

class ParentOrg(models.Model):
    parent_organization_lbn = models.CharField(max_length=70)
    parent_organization_tin = models.CharField(max_length=9)
# end ParentOrg

class AuthorizedOfficial(models.Model):
    first_name = models.CharField(max_length=20)
    middle_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=35)
    name_suffix_text = models.CharField(max_length=5)
    name_prefix_text = models.CharField(max_length=5)
    credential_text = models.CharField(max_length=20)
    title_or_position = models.CharField(max_length=35)
    telephone_number = models.CharField(max_length=20)
# end AuthorizedOfficial

class ContactInfo(models.Model):
    mailing_address_telephone_number = models.CharField(max_length=20)
    practice_address_telephone_number = models.CharField(max_length=20)
    mailing_address_fax_number = models.CharField(max_length=20)
    practice_address_fax_number = models.CharField(max_length=20)
# end ContactInfo

class NPI_Details(models.Model):
    provider_enumeration_date = models.DateField(blank=True,null=True)
    last_update_date = models.DateField(blank=True,null=True)
    npi_deactivation_date = models.DateField(blank=True,null=True)
    npi_deactivation_reason_code = models.CharField(max_length=2)
    npi_reactivation_date = models.DateField(blank=True,null=True)
# end NPI_Details

class Individual(models.Model):
    first_name = models.CharField(max_length=20)
    middle_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=35)
    name_suffix_text = models.CharField(max_length=5)
    name_prefix_text = models.CharField(max_length=5)
    credential_text = models.CharField(max_length=20)

    other_first_name = models.CharField(max_length=20)
    other_middle_name = models.CharField(max_length=20)
    other_last_name = models.CharField(max_length=35)
    other_name_suffix_text = models.CharField(max_length=5)
    other_name_prefix_text = models.CharField(max_length=5)
    other_credential_text = models.CharField(max_length=20)
    other_last_name_type_code = models.PositiveSmallIntegerField()

    gender_code = models.CharField(max_length=1)
    is_sole_proprietor = models.CharField(max_length=1)

    def __unicode__(self):
        return u'%s %s' % (self.first_name, self.last_name)
# end Individual
