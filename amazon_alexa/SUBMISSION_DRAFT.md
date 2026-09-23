# Amazon Devpost Submission Draft

This file contains only fields that can be prepared without inventing personal attestations.

## Ready answers

28285 Submitter Type  
Individual — based on the registered solo entry.

28286 Organization Name  
N/A

28289 Primary Track  
Alexa+

28290 Code Repository  
https://github.com/jpadilla987-png/lead-rescue-agent/tree/amazon-alexa

28291 New or existing prior to August 31, 2026?  
Existing, but significantly updated.

28292 Significant update explanation  
The original repository predates the hackathon. During the submission window the amazon-alexa branch added the Alexa+/MCP implementation, Streamable HTTP server, transparent lead-priority tools, guarded follow-up behavior, protocol-version compatibility assertion, browser simulation, adversarial tests, security scanning, friction log, demo plan, and release-quality tooling.

28293 AWS Builder Mini Challenge  
No

28294 AWS Builder description  
N/A — not entering the AWS Builder Mini Challenge.

28295 Open Source Mini Challenge  
Yes

28296 Contribution URL  
https://github.com/jpadilla987-png/lead-rescue-agent/tree/amazon-alexa

28297 Project Repository URL  
https://github.com/jpadilla987-png/lead-rescue-agent

28298 GitHub Username  
jpadilla987-png

28299 Open Source description  
The amazon-alexa branch is a new public contribution created during the hackathon window. It adds a self-hosted MCP implementation, Streamable HTTP transport, transparent lead-priority tools, guarded follow-up behavior, a judge-facing Alexa+ style simulation, adversarial and protocol compatibility tests, security scanning, and reusable quality tooling. It matters because service businesses can recover high-value leads while keeping pricing and unusual commitments under owner control.

28300 Optional Feature Request  
Important: provide an Alexa+ self-hosted MCP starter that includes a negotiated protocol-version assertion, safe local-vs-public host defaults, and a minimal end-to-end compatibility test.

28301 Optional Friction Log  
https://github.com/jpadilla987-png/lead-rescue-agent/blob/amazon-alexa/amazon_alexa/FRICTION_LOG.md

28303 Feedback Q1  
MCP Python SDK v2 for the self-hosted MCP server, tool/prompt registration, Streamable HTTP transport, and client smoke testing; Python unittest for deterministic behavior and adversarial checks; GitHub Actions for reproducible CI and security review; vanilla HTML/CSS/JavaScript for the judge-facing Alexa+ style simulation.

28304 Feedback Q2  
The MCP Python SDK kept the tool surface compact and readable. The same implementation could be tested in-process and over Streamable HTTP, and the connected client exposes protocol metadata. GitHub Actions made functional, adversarial, dependency, static-security, CodeQL, and release-gate evidence repeatable.

28305 Feedback Q3  
The main friction was proving the exact minimum protocol revision rather than merely proving a successful tool call. A successful Streamable HTTP smoke test did not initially expose the negotiated revision in its output. A starter that asserts protocol compatibility and distinguishes safe local host defaults from intentional public deployment would reduce uncertainty.

28306 Feedback Q4  
Getting from zero to a working MCP tool surface was fast once the current SDK API was established. The slower part was converting “it runs” into evidence that it satisfies the exact hackathon transport and protocol requirement. Those checks are now automated in CI.

28307 Feedback Q5  
Yes. The MCP tool model is a strong fit for bounded business actions because the callable surface is explicit and testable. I would use it again with protocol-version, adversarial, and security checks included from the start.

## Human/account gates — do not infer

28287 Submitter Country of Residence  
NEEDS JOSE

28288 Canada Province / N/A  
NEEDS COUNTRY ANSWER FIRST

28308 Age checkbox  
NEEDS JOSE'S EXPLICIT CONFIRMATION

28309 Eligible Jurisdiction checkbox  
NEEDS JOSE'S EXPLICIT CONFIRMATION

28310 Employee checkbox  
NEEDS JOSE'S EXPLICIT CONFIRMATION

Required demo video URL  
NEEDS PUBLIC YOUTUBE OR VIMEO URL after final recording/upload.

Optional Project Testing Link  
Public hosting attempted through GitHub Pages, but the connected GitHub integration cannot enable Pages administration. Website is optional under the current submission requirements.
