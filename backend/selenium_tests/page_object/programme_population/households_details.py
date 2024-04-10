from page_object.base_components import BaseComponents
from selenium.webdriver.remote.webelement import WebElement


class HouseholdsDetails(BaseComponents):
    pageHeaderContainer = 'div[data-cy="page-header-container"]'
    pageHeaderTitle = 'h5[data-cy="page-header-title"]'
    labelHouseholdSize = 'div[data-cy="label-Household Size"]'
    labelResidenceStatus = 'div[data-cy="label-Residence Status"]'
    labelHeadOfHousehold = 'div[data-cy="label-Head of Household"]'
    labelFemaleChildHeadedHousehold = 'div[data-cy="label-FEMALE CHILD HEADED HOUSEHOLD"]'
    labelChildHeadedHousehold = 'div[data-cy="label-CHILD HEADED HOUSEHOLD"]'
    labelCountry = 'div[data-cy="label-Country"]'
    labelCountryOfOrigin = 'div[data-cy="label-Country of Origin"]'
    labelAddress = 'div[data-cy="label-Address"]'
    labelVillage = 'div[data-cy="label-Village"]'
    labelZipCode = 'div[data-cy="label-Zip code"]'
    labelAdministrativeLevel1 = 'div[data-cy="label-Administrative Level 1"]'
    labelAdministrativeLevel2 = 'div[data-cy="label-Administrative Level 2"]'
    labelAdministrativeLevel3 = 'div[data-cy="label-Administrative Level 3"]'
    labelAdministrativeLevel4 = 'div[data-cy="label-Administrative Level 4"]'
    labelGeolocation = 'div[data-cy="label-Geolocation"]'
    labelUnhcrCaseId = 'div[data-cy="label-UNHCR CASE ID"]'
    labelLengthOfTimeSinceArrival = 'div[data-cy="label-LENGTH OF TIME SINCE ARRIVAL"]'
    labelNumberOfTimesDisplaced = 'div[data-cy="label-NUMBER OF TIMES DISPLACED"]'
    labelIsThisAReturneeHousehold = 'div[data-cy="label-IS THIS A RETURNEE HOUSEHOLD?"]'
    labelLinkedGrievances = 'div[data-cy="label-Linked Grievances"]'
    labelDataCollectingType = 'div[data-cy="label-Data Collecting Type"]'
    labelCashReceived = 'div[data-cy="label-Cash received"]'
    labelTotalCashReceived = 'div[data-cy="label-Total Cash Received"]'
    tableTitle = 'h6[data-cy="table-title"]'
    tableLabel = 'span[data-cy="table-label"]'
    statusContainer = 'div[data-cy="status-container"]'
    tablePagination = 'div[data-cy="table-pagination"]'
    tableRow = 'tr[data-cy="table-row"]'
    labelSource = 'div[data-cy="label-Source"]'
    labelImportName = 'div[data-cy="label-Import name"]'
    labelRegistrationDate = 'div[data-cy="label-Registration Date"]'
    labelUserName = 'div[data-cy="label-User name"]'

    def getBusinessAreaContainer(self) -> WebElement:
        return self.wait_for(self.businessAreaContainer)

    def getGlobalProgramFilterContainer(self) -> WebElement:
        return self.wait_for(self.globalProgramFilterContainer)

    def getGlobalProgramFilter(self) -> WebElement:
        return self.wait_for(self.globalProgramFilter)

    def getMenuUserProfile(self) -> WebElement:
        return self.wait_for(self.menuUserProfile)

    def getSideNav(self) -> WebElement:
        return self.wait_for(self.sideNav)

    def getNavCountryDashboard(self) -> WebElement:
        return self.wait_for(self.navCountryDashboard)

    def getNavRegistrationDataImport(self) -> WebElement:
        return self.wait_for(self.navRegistrationDataImport)

    def getNavProgrammePopulation(self) -> WebElement:
        return self.wait_for(self.navProgrammePopulation)

    def getNavHouseholds(self) -> WebElement:
        return self.wait_for(self.navHouseholds)

    def getNavIndividuals(self) -> WebElement:
        return self.wait_for(self.navIndividuals)

    def getNavProgrammeManagement(self) -> WebElement:
        return self.wait_for(self.navProgrammeManagement)

    def getNavProgrammeDetails(self) -> WebElement:
        return self.wait_for(self.navProgrammeDetails)

    def getNavTargeting(self) -> WebElement:
        return self.wait_for(self.navTargeting)

    def getNavCashAssist(self) -> WebElement:
        return self.wait_for(self.navCashAssist)

    def getNavPaymentVerification(self) -> WebElement:
        return self.wait_for(self.navPaymentVerification)

    def getNavGrievance(self) -> WebElement:
        return self.wait_for(self.navGrievance)

    def getNavGrievanceTickets(self) -> WebElement:
        return self.wait_for(self.navGrievanceTickets)

    def getNavGrievanceDashboard(self) -> WebElement:
        return self.wait_for(self.navGrievanceDashboard)

    def getNavFeedback(self) -> WebElement:
        return self.wait_for(self.navFeedback)

    def getNavProgrammeUsers(self) -> WebElement:
        return self.wait_for(self.navProgrammeUsers)

    def getNavActivityLog(self) -> WebElement:
        return self.wait_for(self.navActivityLog)

    def getNavResourcesKnowledgeBase(self) -> WebElement:
        return self.wait_for(self.navResourcesKnowledgeBase)

    def getNavResourcesConversations(self) -> WebElement:
        return self.wait_for(self.navResourcesConversations)

    def getNavResourcesToolsAndMaterials(self) -> WebElement:
        return self.wait_for(self.navResourcesToolsAndMaterials)

    def getNavResourcesReleaseNote(self) -> WebElement:
        return self.wait_for(self.navResourcesReleaseNote)

    def getPageHeaderContainer(self) -> WebElement:
        return self.wait_for(self.pageHeaderContainer)

    def getPageHeaderTitle(self) -> WebElement:
        return self.wait_for(self.pageHeaderTitle)

    def getLabelHouseholdSize(self) -> WebElement:
        return self.wait_for(self.labelHouseholdSize)

    def getLabelResidenceStatus(self) -> WebElement:
        return self.wait_for(self.labelResidenceStatus)

    def getLabelHeadOfHousehold(self) -> WebElement:
        return self.wait_for(self.labelHeadOfHousehold)

    def getLabelFemaleChildHeadedHousehold(self) -> WebElement:
        return self.wait_for(self.labelFemaleChildHeadedHousehold)

    def getLabelChildHeadedHousehold(self) -> WebElement:
        return self.wait_for(self.labelChildHeadedHousehold)

    def getLabelCountry(self) -> WebElement:
        return self.wait_for(self.labelCountry)

    def getLabelCountryOfOrigin(self) -> WebElement:
        return self.wait_for(self.labelCountryOfOrigin)

    def getLabelAddress(self) -> WebElement:
        return self.wait_for(self.labelAddress)

    def getLabelVillage(self) -> WebElement:
        return self.wait_for(self.labelVillage)

    def getLabelZipCode(self) -> WebElement:
        return self.wait_for(self.labelZipCode)

    def getLabelAdministrativeLevel1(self) -> WebElement:
        return self.wait_for(self.labelAdministrativeLevel1)

    def getLabelAdministrativeLevel2(self) -> WebElement:
        return self.wait_for(self.labelAdministrativeLevel2)

    def getLabelAdministrativeLevel3(self) -> WebElement:
        return self.wait_for(self.labelAdministrativeLevel3)

    def getLabelAdministrativeLevel4(self) -> WebElement:
        return self.wait_for(self.labelAdministrativeLevel4)

    def getLabelGeolocation(self) -> WebElement:
        return self.wait_for(self.labelGeolocation)

    def getLabelUnhcrCaseId(self) -> WebElement:
        return self.wait_for(self.labelUnhcrCaseId)

    def getLabelLengthOfTimeSinceArrival(self) -> WebElement:
        return self.wait_for(self.labelLengthOfTimeSinceArrival)

    def getLabelNumberOfTimesDisplaced(self) -> WebElement:
        return self.wait_for(self.labelNumberOfTimesDisplaced)

    def getLabelIsThisAReturneeHousehold(self) -> WebElement:
        return self.wait_for(self.labelIsThisAReturneeHousehold)

    def getLabelLinkedGrievances(self) -> WebElement:
        return self.wait_for(self.labelLinkedGrievances)

    def getLabelDataCollectingType(self) -> WebElement:
        return self.wait_for(self.labelDataCollectingType)

    def getLabelCashReceived(self) -> WebElement:
        return self.wait_for(self.labelCashReceived)

    def getLabelTotalCashReceived(self) -> WebElement:
        return self.wait_for(self.labelTotalCashReceived)

    def getTableTitle(self) -> WebElement:
        return self.wait_for(self.tableTitle)

    def getTableLabel(self) -> WebElement:
        return self.wait_for(self.tableLabel)

    def getStatusContainer(self) -> WebElement:
        return self.wait_for(self.statusContainer)

    def getTablePagination(self) -> WebElement:
        return self.wait_for(self.tablePagination)

    def getTableRow(self) -> WebElement:
        return self.wait_for(self.tableRow)

    def getLabelSource(self) -> WebElement:
        return self.wait_for(self.labelSource)

    def getLabelImportName(self) -> WebElement:
        return self.wait_for(self.labelImportName)

    def getLabelRegistrationDate(self) -> WebElement:
        return self.wait_for(self.labelRegistrationDate)

    def getLabelUserName(self) -> WebElement:
        return self.wait_for(self.labelUserName)
