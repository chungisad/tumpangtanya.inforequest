# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s tumpangtanya.inforequest -t test_form_a_submission_document.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src tumpangtanya.inforequest.testing.TUMPANGTANYA_INFOREQUEST_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot /src/tumpangtanya/inforequest/tests/robot/test_form_a_submission_document.robot
#
# See the http://docs.plone.org for further details (search for robot
# framework).
#
# ============================================================================

*** Settings *****************************************************************

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Open test browser
Test Teardown  Close all browsers


*** Test Cases ***************************************************************

Scenario: As a site administrator I can add a Form A Submission Document
  Given a logged-in site administrator
    and an add Info Request form
   When I type 'My Form A Submission Document' into the title field
    and I submit the form
   Then a Form A Submission Document with the title 'My Form A Submission Document' has been created

Scenario: As a site administrator I can view a Form A Submission Document
  Given a logged-in site administrator
    and a Form A Submission Document 'My Form A Submission Document'
   When I go to the Form A Submission Document view
   Then I can see the Form A Submission Document title 'My Form A Submission Document'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add Info Request form
  Go To  ${PLONE_URL}/++add++Info Request

a Form A Submission Document 'My Form A Submission Document'
  Create content  type=Info Request  id=my-form_a_submission_document  title=My Form A Submission Document

# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.IBasic.title  ${title}

I submit the form
  Click Button  Save

I go to the Form A Submission Document view
  Go To  ${PLONE_URL}/my-form_a_submission_document
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a Form A Submission Document with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the Form A Submission Document title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
