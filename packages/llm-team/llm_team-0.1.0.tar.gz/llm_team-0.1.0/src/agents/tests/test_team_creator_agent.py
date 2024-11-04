import re
import unittest
from typing import Dict, List

from src.agents.team_creation import parse_agents, parse_workflow


class TestAgentParser(unittest.TestCase):

    def test_valid_input(self):
        input_xml = "<Agent> <Title>Valid Agent</Title> <Responsibility and Objectives>Valid Resp</Responsibility and Objectives> </Agent>"
        expected_output = [{
            "title": "Valid Agent",
            "responsibility_and_objectives": "Valid Resp"
        }]
        self.assertEqual(parse_agents(input_xml), expected_output)

    def test_multiple_agents(self):
        input_xml = """
        <Agent> <Title>Agent 1</Title> <Responsibility and Objectives>Resp 1</Responsibility and Objectives> </Agent>
        <Agent> <Title>Agent 2</Title> <Responsibility and Objectives>Resp 2</Responsibility and Objectives> </Agent>
        """
        expected_output = [{
            "title": "Agent 1",
            "responsibility_and_objectives": "Resp 1"
        }, {
            "title": "Agent 2",
            "responsibility_and_objectives": "Resp 2"
        }]
        self.assertEqual(parse_agents(input_xml), expected_output)

    def test_empty_input(self):
        with self.assertRaises(Exception):
            parse_agents("")

    def test_whitespace_only_input(self):
        with self.assertRaises(Exception):
            parse_agents("   \n  \t  ")

    def test_non_string_input(self):
        with self.assertRaises(Exception):
            parse_agents(123)  # type: ignore

    def test_missing_responsibility(self):
        input_xml = "<Agent> <Title>No Resp</Title> </Agent>"
        expected_output = [{
            "title": "No Resp",
            "responsibility_and_objectives": ""
        }]
        self.assertEqual(parse_agents(input_xml), expected_output)

    def test_missing_title(self):
        input_xml = "<Agent> <Responsibility and Objectives>No Title</Responsibility and Objectives> </Agent>"
        expected_output = [{
            "title": "",
            "responsibility_and_objectives": "No Title"
        }]
        self.assertEqual(parse_agents(input_xml), expected_output)

    def test_invalid_structure(self):
        input_xml = "<InvalidTag>Invalid Input</InvalidTag>"
        self.assertEqual(parse_agents(input_xml), [])

    def test_partial_valid_content(self):
        input_xml = """
        <Agent> <Title>Valid Agent</Title> <Responsibility and Objectives>Valid Resp</Responsibility and Objectives> </Agent>
        <InvalidAgent> Invalid Content </InvalidAgent>
        <Agent> <Title>Another Valid</Title> <Responsibility and Objectives>Another Resp</Responsibility and Objectives> </Agent>
        """
        expected_output = [{
            "title": "Valid Agent",
            "responsibility_and_objectives": "Valid Resp"
        }, {
            "title": "Another Valid",
            "responsibility_and_objectives": "Another Resp"
        }]
        self.assertEqual(parse_agents(input_xml), expected_output)


class TestParseWorkflow(unittest.TestCase):

    def test_valid_workflow(self):
        xml_string = '''
        <SomeOtherTags>
            <Workflow>
                <Step1>Do something</Step1>
                <Step2>Do something else</Step2>
            </Workflow>
        </SomeOtherTags>
        '''
        expected_output = '''
                <Step1>Do something</Step1>
                <Step2>Do something else</Step2>
        '''
        self.assertEqual(
            parse_workflow(xml_string).strip(), expected_output.strip())

    def test_no_workflow(self):
        xml_string = '''
        <SomeOtherTags>
            <NotAWorkflow>
                <Step1>Do something</Step1>
                <Step2>Do something else</Step2>
            </NotAWorkflow>
        </SomeOtherTags>
        '''
        with self.assertRaises(Exception):
            parse_workflow(xml_string)

    def test_empty_workflow(self):
        xml_string = '<Workflow></Workflow>'
        self.assertEqual(parse_workflow(xml_string), "")

    def test_multiple_workflows(self):
        xml_string = '''
        <SomeOtherTags>
            <Workflow>
                <Step1>First workflow</Step1>
            </Workflow>
            <Workflow>
                <Step1>Second workflow</Step1>
            </Workflow>
        </SomeOtherTags>
        '''
        expected_output = '''
                <Step1>First workflow</Step1>
        '''
        self.assertEqual(
            parse_workflow(xml_string).strip(), expected_output.strip())


if __name__ == '__main__':
    unittest.main()
