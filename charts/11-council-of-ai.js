graph TB
    %% Define styles
    classDef actor fill:#f9f,stroke:#333,stroke-width:2px,color:black;
    classDef router fill:#cce5ff,stroke:#007bff,stroke-width:2px,color:black;
    classDef models fill:#e2e6ea,stroke:#333,stroke-width:1px,color:black;
    classDef output fill:#d4edda,stroke:#28a745,stroke-width:2px,color:black;

    %% Nodes
    PE[Prompt Engineer PE]:::actor
    ComplexQuery[Complex Query Requiring Consensus]
    Orchestrator{Orchestration Layer / Router}:::router

    subgraph "The Council of AI (Model Pool)"
        OAI[OpenAI]:::models
        Gem[Gemini]:::models
        Meta[MetaAI]:::models
        Grok[Grok]:::models
        Deep[DeepSeek]:::models
        IBM[IBM Watson]:::models
    end
    
    Synthesis[Synthesis Agent / Judge]:::router
    FinalOutput[Composite Consolidated Response]:::output
    InteractiveMode[Alternative: Interactive Discussion Forum]:::output

    %% Connections
    PE --> ComplexQuery
    ComplexQuery --> Orchestrator

    %% Parallel Processing
    Orchestrator --"Broadcast Query"--> OAI
    Orchestrator --> Gem
    Orchestrator --> Meta
    Orchestrator --> Grok
    Orchestrator --> Deep
    Orchestrator --> IBM

    %% Path A: Consolidation
    OAI --> Synthesis
    Gem --> Synthesis
    Meta --> Synthesis
    Grok --> Synthesis
    Deep --> Synthesis
    IBM --> Synthesis

    Synthesis -->|Consolidate & Verify| FinalOutput
    FinalOutput --> PE

    %% Path B: Interaction (Dotted line for alternative mode)
    Orchestrator -.->|Enable Debate Mode| InteractiveMode
    OAI <.-> InteractiveMode
    Gem <.-> InteractiveMode
    Meta <.-> InteractiveMode
    InteractiveMode -.->|Generated Forum Transcript| PE