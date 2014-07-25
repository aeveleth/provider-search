from django.shortcuts import render
from django.http import HttpResponse
from providers.models import Provider, Individual, Organization, Taxonomy, PracticeAddress, ContactInfo

# Create your views here.
def search(request):
    results = []

    if 'search_individual' in request.GET:
        results = getResults(request, False)

        return render(request, 'search_results.html', {'results_list' : results, 'organization' : False})
    elif 'search_organization' in request.GET:
        results = getResults(request, True)

        return render(request, 'search_results.html', {'results_list' : results, 'organization' : True})
    else:
        states = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'DC', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']
        return render(request, 'search_form.html', {'states' : states})
    # end if
# end search

def getResults(request, organization):
    if organization:
        provider_results = Provider.objects.filter(entity_type_code=2)
        organization_results = Organization.objects.all()
        prefix = 'organization_'
        organization_name_query = request.GET.get(prefix + 'name', '').upper()
        if organization_name_query:
            organization_results = Organization.objects.filter(organization_name__contains=organization_name_query)
            organization_npis = [organization.pk for organization in organization_results]
            provider_results = provider_results.filter(npi__in=organization_npis)
    else:
        provider_results = Provider.objects.filter(entity_type_code=1)
        individual_results = Individual.objects.all()
        prefix = 'individual_'
        first_name_query = request.GET.get('first_name', '').upper()
        last_name_query = request.GET.get('last_name', '').upper()
        if first_name_query:
            individual_results = individual_results.filter(first_name__contains=first_name_query)
        if last_name_query:
            individual_results = individual_results.filter(last_name__contains=last_name_query)
        if first_name_query or last_name_query:
            individual_npis = [individual.pk for individual in individual_results]
            provider_results = provider_results.filter(npi__in=individual_npis)
    # end if

    taxonomy_results = Taxonomy.objects.all()
    address_results = PracticeAddress.objects.all()

    npi_query = request.GET.get(prefix + 'npi', '')
    taxonomy_query = request.GET.get(prefix + 'taxonomy', '').upper()
    zip_code_query = request.GET.get(prefix + 'zip', '').replace('-', '')
    state_query = request.GET.get(prefix + 'state', '').upper()

    if npi_query or taxonomy_query or zip_code_query or state_query:
        if npi_query:
            provider_results = provider_results.filter(npi=npi_query)

        if taxonomy_query:
            taxonomy_results = taxonomy_results.filter(taxonomy_code=taxonomy_query)

        if len(zip_code_query) == 5:
            address_results = address_results.filter(postal_code__startswith=zip_code_query)
        elif zip_code_query:
            address_results = address_results.filter(postal_code=zip_code_query)
        if state_query:
            address_results = address_results.filter(state_name=state_query)

        taxonomy_pks = [taxonomy.pk for taxonomy in taxonomy_results]
        address_npis = [address.pk for address in address_results]
        provider_results = provider_results.filter(pk__in=taxonomy_pks).filter(npi__in=address_npis)
    # end if

    results = []
    for provider in provider_results:
        npi = provider.npi
        taxonomy_code = taxonomy_results.get(pk=provider.pk).taxonomy_code
        address = address_results.get(pk=npi)
        phone_number = ContactInfo.objects.get(pk=npi).practice_address_telephone_number
        if organization:
            organization_name = organization_results.get(pk=npi).organization_name
            results.append(OrganizationResult(npi, organization_name, taxonomy_code, address, phone_number))
        else:
            individual = individual_results.get(pk=npi)
            results.append(IndividualResult(npi, individual, taxonomy_code, address, phone_number))
        # end if
    # end for

    return results
# end getProviderResults

class Result(object):
    def __init__(self, npi, taxonomy_code, address, phone_number):
        self.npi = npi
        self.taxonomy_code = taxonomy_code

        self.address = ''
        for x in address.address_first_line.split():
            self.address += ' ' + x.capitalize()
        if address.address_second_line != 'NULL':
            self.address += '\n'
            for x in address.address_second_line.split():
                self.address += ' ' + x.capitalize()
        # end if
        self.address = self.address[1:]

        self.city = ''
        for x in address.city_name.split():
            self.city += ' ' + x.capitalize()
        self.city = self.city[1:]
        self.state = address.state_name

        if len(address.postal_code) == 9:
            self.zip_code = address.postal_code[0:5] + '-' + address.postal_code[5:]
        else:
            self.zip_code = address.postal_code
        # end if

        if len(phone_number) == 10:
            self.phone_number = phone_number[0:3] + '-' + phone_number[3:6] + '-' + phone_number[6:]
        else:
            self.phone_number = phone_number
        # end if
    # end __init__
# end Result

class IndividualResult(Result):
    def __init__(self, npi, individual, taxonomy_code, address, phone_number):
        self.first_name = individual.first_name.capitalize()
        self.last_name = individual.last_name.capitalize()
        self.credential_text = individual.credential_text if individual.credential_text != 'NULL' else ''
        super(IndividualResult, self).__init__(npi, taxonomy_code, address, phone_number)
    # end __init__
# end IndividualResult

class OrganizationResult(Result):
    def __init__(self, npi, organization_name, taxonomy_code, address, phone_number):
        self.organization_name = ''
        temp = organization_name.split()
        for x in temp:
            self.organization_name += ' ' + x.capitalize()
        self.organization_name = self.organization_name[1:].replace('\\', '')
        super(OrganizationResult, self).__init__(npi, taxonomy_code, address, phone_number)
    # end __init__
# end OrganizationResult

