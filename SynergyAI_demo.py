from llm_client import LLMClient
from utils import read_markdown_file


def optimize_document_with_virtual_roundtable(document):
    client = LLMClient.get_instance()
    
    print("\n=== Starting Virtual Roundtable Discussion ===\n")
    
    # Define experts
    experts = {
        "product_manager": "作为资深软件产品经理，请仔细审阅以下文档，从产品角度提出关键问题：\n\n{document}\n\n请列出主要问题：",
        "developer": "作为资深软件开发工程师，请仔细审阅以下文档，从技术实现角度提出关键问题：\n\n{document}\n\n请列出主要问题："
    }
    
    # Problem identification phase
    print("Phase 1: Initial Problem Identification")
    problems = {}
    for role, prompt in experts.items():
        print(f"\n{role.title()} is analyzing the document...")
        response = client.ask(prompt.format(document=document))
        problems[role] = response
        print(f"{role.title()}'s issues:\n{response}")
    
    # Problem discussion phase
    print("\nPhase 2: Discussion Rounds")
    max_rounds = 3
    round_num = 0
    consensus = None
    
    while round_num < max_rounds:
        print(f"\n--- Round {round_num + 1} ---")
        
        print("\nProduct Manager's turn:")
        pm_prompt = """
            讨论轮次 {round}
            文档内容：
            {document}

            产品经理先前提出的问题：
            {pm_issues}

            开发工程师提出的问题：
            {dev_issues}

            作为产品经理，请针对上述问题进行分析和回应："""
        
        pm_response = client.ask(pm_prompt.format(
            round=round_num + 1,
            document=document,
            pm_issues=problems['product_manager'],
            dev_issues=problems['developer']
        ))
        print(pm_response)
        
        print("\nDeveloper's turn:")
        dev_prompt = """
            讨论轮次 {round}
            文档内容：
            {document}

            产品经理的观点：
            {pm_response}

            作为开发工程师，请针对产品经理的观点进行回应："""
        
        dev_response = client.ask(dev_prompt.format(
            round=round_num + 1,
            document=document,
            pm_response=pm_response
        ))
        print(dev_response)
        
        print("\nChecking for consensus...")
        consensus_prompt = """
            基于当前讨论进展：

            文档内容：
            {document}

            产品经理观点：
            {pm_response}

            开发工程师观点：
            {dev_response}

            请分析是否达成共识：
            1. 如果达成共识，请总结共识要点
            2. 如果未达成共识，请回复"继续讨论"并说明分歧点"""

        consensus = client.ask(consensus_prompt.format(
            document=document,
            pm_response=pm_response,
            dev_response=dev_response
        ))
        print(f"Consensus status:\n{consensus}")
        
        if "继续讨论" not in consensus:
            print("\nConsensus reached!")
            break
        
        round_num += 1
    
    if consensus is None or "继续讨论" in consensus:
        consensus = "未在规定轮次内达成完全共识。最后讨论要点：" + consensus
        print("\nMaximum rounds reached without full consensus.")
    
    # Final optimization phase
    print("\nPhase 3: Final Document Optimization")
    final_prompt = """
        基于前述讨论达成的共识：

        原始文档：
        {document}

        讨论共识：
        {consensus}

        请提供优化后的文档版本，需要：
        1. 保持文档原有结构
        2. 整合各方意见
        3. 优化内容表述

        优化后的文档："""

    optimized_document = client.ask(final_prompt.format(
        document=document,
        consensus=consensus
    ))
    
    print("\n=== Virtual Roundtable Discussion Completed ===\n")
    return optimized_document


def main():
    document = read_markdown_file("sample_document.md")
    optimized_document = optimize_document_with_virtual_roundtable(document)
    print(f"Optimized document:\n{optimized_document}")


if __name__ == "__main__":
    main()
