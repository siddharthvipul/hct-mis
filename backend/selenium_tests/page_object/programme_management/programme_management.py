from time import sleep

from page_object.base_components import BaseComponents
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement


class ProgrammeManagement(BaseComponents):
    headerTitle = 'h5[data-cy="page-header-title"]'
    buttonNewProgram = 'a[data-cy="button-new-program"]'
    inputProgrammeName = 'input[data-cy="input-name"]'
    labelProgrammeName = 'div[data-cy="input-programme-name"]'
    inputStartDate = 'input[name="startDate"]'
    labelStartDate = 'div[data-cy="date-picker-filter"]'
    inputEndDate = 'input[name="endDate"]'
    labelEndDate = 'div[data-cy="date-picker-filter"]'
    selectSelector = 'div[data-cy="select-sector"]'
    labelSelector = 'div[data-cy="input-sector"]'
    inputDataCollectingType = 'div[data-cy="input-data-collecting-type"]'
    labelDataCollectingType = 'div[data-cy="input-data-collecting-type"]'
    inputCashPlus = 'span[data-cy="input-cashPlus"]'
    inputDescription = 'textarea[data-cy="input-description"]'
    inputBudget = 'input[data-cy="input-budget"]'
    inputAdministrativeAreasOfImplementation = 'input[data-cy="input-administrativeAreasOfImplementation"]'
    inputPopulation = 'input[data-cy="input-populationGoal"]'
    inputFreqOfPaymentOneOff = '//*[@data-cy="input-frequency-of-payment"]/div[1]/div/span'
    inputFreqOfPaymentRegular = '//*[@data-cy="input-frequency-of-payment"]/div[2]/div/span'
    buttonNext = 'button[data-cy="button-next"]'
    buttonBack = 'button[data-cy="button-back"]'
    buttonCancel = 'a[data-cy="button-cancel"]'
    buttonSave = 'button[data-cy="button-save"]'
    selectPartnerAccess = 'div[data-cy="select-partnerAccess"]'
    buttonAddPartner = 'button[data-cy="button-add-partner"]'
    inputPartner = 'div[data-cy="select-partners[0].id"]'
    buttonDelete = 'button[data-cy="button-delete"]'
    labelAdminArea = '//*[@id="radioGroup-partners[0].areaAccess"]/div[2]/div/span'
    calendarIcon = 'button[data-cy="calendar-icon"]'
    calendar = 'div[data-popper-placement="bottom-start"]'
    calendarMonthYear = (
        '//*[@class="MuiPickersSlideTransition-transitionContainer ' 'MuiPickersCalendarHeader-transitionContainer"]'
    )
    calendarChangeMonth = '//*[@class="MuiButtonBase-root MuiIconButton-root MuiPickersCalendarHeader-iconButton"]'
    calendarDays = (
        '//*[@class="MuiButtonBase-root MuiIconButton-root MuiPickersDay-day" '
        'or @class="MuiButtonBase-root MuiIconButton-root MuiPickersDay-day MuiPickersDay-current '
        'MuiPickersDay-daySelected" '
        'or @class="MuiButtonBase-root MuiIconButton-root MuiPickersDay-day '
        'MuiPickersDay-dayDisabled"]'
    )
    filtersSearch = '//*[@data-cy="filters-search"]/div/input'
    buttonApply = 'button[data-cy="button-filters-clear"]'
    buttonEditProgram = 'a[data-cy="button-edit-program"]'
    inputProgrammeCode = 'input[data-cy="input-programmeCode"]'
    tableRow = 'tr[data-cy="table-row-{}"]'

    def getCalendarIcon(self) -> WebElement:
        return self.wait_for(self.calendarIcon)

    def getCalendar(self) -> WebElement:
        return self.wait_for(self.calendar)

    def chooseAreaAdmin1ByName(self, name: str) -> WebElement:
        return self.wait_for(f"//*[contains(text(), '{name}')]/span", By.XPATH)

    def getLabelAdminArea(self) -> WebElement:
        return self.wait_for(self.labelAdminArea, By.XPATH)

    def getRowByProgramName(self, programName: str) -> WebElement:
        locator = f'tr[data-cy="table-row-{programName}"]'
        self.wait_for(locator)
        return self.get_elements(locator)[0].text.split("\n")

    def getAccessToProgram(self) -> WebElement:
        return self.wait_for(self.selectPartnerAccess)

    def selectWhoAccessToProgram(self, name: str) -> None:
        self.select_option_by_name(name)

    def getButtonAddPartner(self) -> WebElement:
        return self.wait_for(self.buttonAddPartner)

    def getButtonDelete(self) -> WebElement:
        return self.wait_for(self.buttonDelete)

    def getButtonDeletePopup(self) -> WebElement:
        return self.wait_for("/html/body/div[2]/div[3]/div/div[3]/div/button[2]", By.XPATH)

    def choosePartnerOption(self, optionName: str) -> None:
        # Todo: Change undefined to name of Partner
        self.wait_for(self.inputPartner).click()
        self.select_option_by_name(optionName)

    def getInputProgrammeName(self) -> WebElement:
        return self.wait_for(self.inputProgrammeName)

    def getLabelProgrammeName(self) -> WebElement:
        return self.wait_for(self.labelProgrammeName)

    def getInputCashPlus(self) -> WebElement:
        return self.wait_for(self.inputCashPlus)

    def getInputFreqOfPaymentOneOff(self) -> WebElement:
        return self.wait_for(self.inputFreqOfPaymentOneOff, By.XPATH)

    def getInputFreqOfPaymentRegular(self) -> WebElement:
        return self.wait_for(self.inputFreqOfPaymentRegular, By.XPATH)

    def getInputStartDate(self) -> WebElement:
        return self.wait_for(self.inputStartDate)

    def chooseInputStartDateViaCalendar(self, day: int) -> None:
        self.get(self.labelStartDate).find_element(By.TAG_NAME, "button").click()
        self.getCalendar()
        # ToDo: Create additional waiting mechanism
        sleep(1)
        self.get_elements(self.calendarDays, By.XPATH)[day - 1].click()
        self.wait_for_disappear(self.calendar)

    def chooseInputEndDateViaCalendar(self, day: int) -> None:
        self.find_in_element(self.getLabelEndDate(), self.calendarIcon)[0].click()
        self.getCalendar()
        month = self.get(self.calendarMonthYear, By.XPATH).text
        self.get_elements(self.calendarChangeMonth, By.XPATH)[0].click()
        for _ in range(5):
            next_month = self.get(self.calendarMonthYear, By.XPATH).text
            sleep(1)
            if month != next_month:
                break
        self.get_elements(self.calendarDays, By.XPATH)[day - 1].click()
        self.wait_for_disappear(self.calendar)

    def getLabelStartDate(self) -> WebElement:
        return self.get_elements(self.labelStartDate)[0]

    def getInputEndDate(self) -> WebElement:
        return self.wait_for(self.inputEndDate)

    def getLabelEndDate(self) -> WebElement:
        return self.get_elements(self.labelEndDate)[1]

    def getButtonNext(self) -> WebElement:
        return self.wait_for(self.buttonNext)

    def getButtonBack(self) -> WebElement:
        return self.wait_for(self.buttonBack)

    def getButtonCancel(self) -> WebElement:
        return self.wait_for(self.buttonCancel)

    def getButtonSave(self) -> WebElement:
        return self.wait_for(self.buttonSave)

    def chooseOptionSelector(self, optionName: str) -> None:
        self.wait_for(self.selectSelector).click()
        self.select_option_by_name(optionName)

    def getLabelSelector(self) -> WebElement:
        return self.wait_for(self.labelSelector)

    def chooseOptionDataCollectingType(self, optionName: str) -> None:
        self.wait_for(self.inputDataCollectingType).click()
        self.select_option_by_name(optionName)

    def getLabelDataCollectingType(self) -> WebElement:
        return self.wait_for(self.labelDataCollectingType)

    def getHeaderTitle(self) -> WebElement:
        return self.wait_for(self.headerTitle)

    def getButtonNewProgram(self) -> WebElement:
        # Workaround because elements overlapped even though Selenium saw that they were available:
        self.driver.execute_script(
            """
            container = document.querySelector("div[data-cy='main-content']")
            container.scrollBy(0,600)
            """
        )
        return self.wait_for(self.buttonNewProgram)

    def fillFiltersSearch(self, filterText: str) -> None:
        self.wait_for(self.filtersSearch, By.XPATH).send_keys(filterText)
        # ToDo: Delete sleep
        sleep(1)
        self.wait_for(self.filtersSearch, By.XPATH).send_keys(Keys.ENTER)

    def getButtonApply(self) -> WebElement:
        return self.wait_for(self.buttonApply)

    def getButtonEditProgram(self) -> WebElement:
        return self.wait_for(self.buttonEditProgram)

    def getInputProgrammeCode(self) -> WebElement:
        return self.wait_for(self.inputProgrammeCode)

    def getInputDescription(self) -> WebElement:
        return self.wait_for(self.inputDescription)

    def getInputBudget(self) -> WebElement:
        return self.wait_for(self.inputBudget)

    def getInputAdministrativeAreasOfImplementation(self) -> WebElement:
        return self.wait_for(self.inputAdministrativeAreasOfImplementation)

    def getInputPopulation(self) -> WebElement:
        return self.wait_for(self.inputPopulation)

    def getTableRowByProgramName(self, program_name: str) -> WebElement:
        return self.wait_for(self.tableRow.format(program_name))
